#!/usr/bin/env python3
"""
Module de suppression d'arrière-plan pour Toolbox
Supprime automatiquement l'arrière-plan d'une image quelle que soit sa couleur
"""

import argparse
import sys
from pathlib import Path
import numpy as np

# Métadonnées du module
VERSION = "1.0.0"
DESCRIPTION = "Supprime l'arrière-plan des images automatiquement"
AUTHOR = "Toolbox"

def remove_background_color_based(image, tolerance=30):
    """
    Supprime l'arrière-plan basé sur la couleur dominante des bords
    
    Args:
        image: Image PIL
        tolerance: Tolérance de couleur (0-255)
    
    Returns:
        Image avec arrière-plan transparent
    """
    img_array = np.array(image.convert('RGBA'))
    height, width = img_array.shape[:2]
    
    # Échantillonne les pixels des bords pour déterminer la couleur de fond
    edge_pixels = []
    
    # Bord supérieur et inférieur
    edge_pixels.extend(img_array[0, :, :3].tolist())  # Première ligne
    edge_pixels.extend(img_array[-1, :, :3].tolist())  # Dernière ligne
    
    # Bords gauche et droit
    edge_pixels.extend(img_array[:, 0, :3].tolist())  # Première colonne
    edge_pixels.extend(img_array[:, -1, :3].tolist())  # Dernière colonne
    
    # Trouve la couleur la plus commune dans les bords
    edge_pixels = np.array(edge_pixels)
    
    # Utilise la moyenne des pixels de bord comme couleur de référence
    bg_color = np.mean(edge_pixels, axis=0).astype(int)
    
    # Crée un masque pour les pixels similaires à la couleur de fond
    diff = np.abs(img_array[:, :, :3] - bg_color)
    mask = np.all(diff <= tolerance, axis=2)
    
    # Applique la transparence
    img_array[mask, 3] = 0  # Canal alpha à 0 (transparent)
    
    from PIL import Image
    return Image.fromarray(img_array, 'RGBA')

def remove_background_edge_detection(image, blur_radius=5, threshold=50):
    """
    Supprime l'arrière-plan en utilisant la détection de contours
    
    Args:
        image: Image PIL
        blur_radius: Rayon de flou pour la détection
        threshold: Seuil de détection des contours
    
    Returns:
        Image avec arrière-plan transparent
    """
    try:
        import cv2
    except ImportError:
        print("Avertissement: OpenCV non installé, utilisation de la méthode basique")
        return remove_background_color_based(image)
    
    # Convertit en numpy array
    img_rgb = np.array(image.convert('RGB'))
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    
    # Applique un flou gaussien
    blurred = cv2.GaussianBlur(img_gray, (blur_radius*2+1, blur_radius*2+1), 0)
    
    # Détection de contours avec Canny
    edges = cv2.Canny(blurred, threshold, threshold*2)
    
    # Dilatation pour fermer les contours
    kernel = np.ones((3,3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # Trouve les contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Crée un masque basé sur le plus grand contour (supposé être l'objet principal)
    mask = np.zeros(img_gray.shape, dtype=np.uint8)
    if contours:
        # Trouve le contour avec la plus grande aire
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.fillPoly(mask, [largest_contour], 255)
        
        # Applique un flou au masque pour des bords plus doux
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # Convertit l'image en RGBA
    img_rgba = np.array(image.convert('RGBA'))
    
    # Applique le masque au canal alpha
    img_rgba[:, :, 3] = mask
    
    from PIL import Image
    return Image.fromarray(img_rgba, 'RGBA')

def remove_background_smart(image, method='auto', **kwargs):
    """
    Suppression intelligente d'arrière-plan avec choix automatique de méthode
    
    Args:
        image: Image PIL
        method: 'auto', 'color', 'edge', ou 'ai'
        **kwargs: Arguments supplémentaires pour les méthodes
    
    Returns:
        Image avec arrière-plan transparent
    """
    if method == 'auto':
        # Analyse l'image pour choisir la meilleure méthode
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        
        # Si l'image est petite ou a peu de variation, utilise la méthode couleur
        if width * height < 500000:  # Moins de 0.5MP
            method = 'color'
        else:
            # Calcule la variance des couleurs pour déterminer la complexité
            variance = np.var(img_array)
            if variance < 1000:  # Image simple
                method = 'color'
            else:  # Image complexe
                method = 'edge'
    
    if method == 'color':
        return remove_background_color_based(image, kwargs.get('tolerance', 30))
    elif method == 'edge':
        return remove_background_edge_detection(
            image, 
            kwargs.get('blur', 5), 
            kwargs.get('threshold', 50)
        )
    elif method == 'ai':
        return remove_background_ai(image)
    else:
        raise ValueError(f"Méthode inconnue: {method}")

def remove_background_ai(image):
    """
    Suppression d'arrière-plan avec IA (utilise rembg si disponible)
    """
    try:
        import rembg
        from io import BytesIO
        
        # Convertit l'image en bytes
        img_bytes = BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Supprime l'arrière-plan avec rembg
        output = rembg.remove(img_bytes.getvalue())
        
        # Convertit le résultat en image PIL
        from PIL import Image
        result_image = Image.open(BytesIO(output))
        return result_image
        
    except ImportError:
        print("Avertissement: rembg non installé, utilisation de la méthode alternative")
        print("Pour installer: pip install rembg")
        return remove_background_smart(image, method='edge')

def process_image(input_path, output_path, method='auto', tolerance=30, 
                 blur=5, threshold=50, preview=False):
    """
    Traite une image pour supprimer son arrière-plan
    
    Args:
        input_path: Chemin de l'image source
        output_path: Chemin de l'image de destination
        method: Méthode à utiliser ('auto', 'color', 'edge', 'ai')
        tolerance: Tolérance de couleur pour la méthode 'color'
        blur: Rayon de flou pour la méthode 'edge'
        threshold: Seuil pour la méthode 'edge'
        preview: Affiche un aperçu avant/après
    
    Returns:
        bool: True si succès, False sinon
    """
    try:
        from PIL import Image
    except ImportError:
        print("Erreur: Le module Pillow n'est pas installé.")
        print("Installez-le avec: pip install Pillow")
        return False
    
    try:
        # Ouvre l'image source
        with Image.open(input_path) as img:
            print(f"Image source: {img.size[0]}x{img.size[1]} pixels, mode: {img.mode}")
            
            # Supprime l'arrière-plan
            print(f"Suppression de l'arrière-plan (méthode: {method})...")
            
            result = remove_background_smart(
                img, 
                method=method,
                tolerance=tolerance,
                blur=blur,
                threshold=threshold
            )
            
            # Sauvegarde le résultat
            result.save(output_path, format='PNG')
            print(f"Image sauvegardée: {output_path}")
            
            # Affiche les statistiques
            original_size = Path(input_path).stat().st_size
            new_size = Path(output_path).stat().st_size
            
            print(f"Taille originale: {original_size / 1024:.1f} KB")
            print(f"Taille finale: {new_size / 1024:.1f} KB")
            
            if preview:
                try:
                    # Affiche un aperçu si possible
                    img.show(title="Original")
                    result.show(title="Sans arrière-plan")
                except:
                    print("Aperçu non disponible sur ce système")
            
            return True
            
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
        return False

def main(args):
    """Point d'entrée principal du module"""
    parser = argparse.ArgumentParser(
        description="Suppression d'arrière-plan d'images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Méthodes disponibles:
  auto    - Choix automatique de la meilleure méthode (défaut)
  color   - Basée sur la couleur dominante des bords
  edge    - Basée sur la détection de contours (nécessite OpenCV)
  ai      - Utilise l'IA (nécessite rembg)

Exemples:
  toolbox run bg_remover photo.jpg photo_nobg.png
  toolbox run bg_remover image.png result.png --method color --tolerance 50
  toolbox run bg_remover portrait.jpg clean.png --method ai
  toolbox run bg_remover pic.jpg out.png --preview

Installation des dépendances optionnelles:
  pip install opencv-python  # Pour la méthode 'edge'
  pip install rembg          # Pour la méthode 'ai'
        """
    )
    
    parser.add_argument('input', help='Fichier image source')
    parser.add_argument('output', help='Fichier image de destination (PNG recommandé)')
    
    parser.add_argument('--method', '-m', choices=['auto', 'color', 'edge', 'ai'],
                       default='auto', help='Méthode de suppression (défaut: auto)')
    
    parser.add_argument('--tolerance', '-t', type=int, default=30,
                       help='Tolérance de couleur pour méthode "color" (0-255, défaut: 30)')
    
    parser.add_argument('--blur', '-b', type=int, default=5,
                       help='Rayon de flou pour méthode "edge" (défaut: 5)')
    
    parser.add_argument('--threshold', type=int, default=50,
                       help='Seuil de détection pour méthode "edge" (défaut: 50)')
    
    parser.add_argument('--preview', '-p', action='store_true',
                       help='Affiche un aperçu du résultat')
    
    # Parse les arguments
    parsed_args = parser.parse_args(args)
    
    # Vérifie que le fichier source existe
    if not Path(parsed_args.input).exists():
        print(f"Erreur: Le fichier '{parsed_args.input}' n'existe pas")
        return 1
    
    # Vérifie les paramètres
    if not 0 <= parsed_args.tolerance <= 255:
        print("Erreur: La tolérance doit être entre 0 et 255")
        return 1
    
    if parsed_args.blur < 1:
        print("Erreur: Le rayon de flou doit être positif")
        return 1
    
    # S'assure que le fichier de sortie a l'extension PNG pour la transparence
    output_path = Path(parsed_args.output)
    if output_path.suffix.lower() not in ['.png']:
        print("Avertissement: Format PNG recommandé pour préserver la transparence")
        response = input("Continuer quand même? (o/N): ")
        if response.lower() not in ['o', 'oui', 'y', 'yes']:
            return 0
    
    # Traite l'image
    success = process_image(
        parsed_args.input,
        parsed_args.output,
        method=parsed_args.method,
        tolerance=parsed_args.tolerance,
        blur=parsed_args.blur,
        threshold=parsed_args.threshold,
        preview=parsed_args.preview
    )
    
    if success:
        print("Suppression d'arrière-plan réussie!")
        return 0
    else:
        return 1

# Test direct du module
if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))