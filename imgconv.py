#!/usr/bin/env python3
"""
Module de conversion d'images pour Toolbox
Convertit les images entre différents formats (JPG, PNG, WEBP, etc.)
"""

import argparse
import sys
from pathlib import Path

# Métadonnées du module
VERSION = "1.0.0"
DESCRIPTION = "Convertit les images entre différents formats"
AUTHOR = "Toolbox"

def convert_image(input_path: str, output_path: str, quality: int = 95):
    """
    Convertit une image d'un format à un autre
    
    Args:
        input_path: Chemin de l'image source
        output_path: Chemin de l'image de destination
        quality: Qualité de compression (pour JPEG)
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
            # Détermine le format de sortie basé sur l'extension
            output_format = Path(output_path).suffix.lower()
            
            # Gère les cas spéciaux
            if output_format in ['.jpg', '.jpeg']:
                # Convertit en RGB si nécessaire (JPEG ne supporte pas la transparence)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Crée un fond blanc
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if 'A' in img.mode else None)
                    img = background
                img.save(output_path, format='JPEG', quality=quality, optimize=True)
            
            elif output_format == '.png':
                img.save(output_path, format='PNG', optimize=True)
            
            elif output_format == '.webp':
                img.save(output_path, format='WEBP', quality=quality, optimize=True)
            
            elif output_format == '.bmp':
                # Convertit en RGB pour BMP
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                img.save(output_path, format='BMP')
            
            else:
                # Essaie de sauvegarder dans le format détecté automatiquement
                img.save(output_path)
        
        return True
        
    except Exception as e:
        print(f"Erreur lors de la conversion: {e}")
        return False

def get_image_info(image_path: str):
    """Affiche les informations d'une image"""
    try:
        from PIL import Image
    except ImportError:
        print("Erreur: Le module Pillow n'est pas installé.")
        return False
    
    try:
        with Image.open(image_path) as img:
            print(f"Fichier: {image_path}")
            print(f"Format: {img.format}")
            print(f"Mode: {img.mode}")
            print(f"Taille: {img.size[0]}x{img.size[1]} pixels")
            
            # Taille du fichier
            file_size = Path(image_path).stat().st_size
            if file_size < 1024:
                print(f"Taille du fichier: {file_size} bytes")
            elif file_size < 1024 * 1024:
                print(f"Taille du fichier: {file_size / 1024:.1f} KB")
            else:
                print(f"Taille du fichier: {file_size / (1024 * 1024):.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors de la lecture de l'image: {e}")
        return False

def main(args):
    """Point d'entrée principal du module"""
    parser = argparse.ArgumentParser(
        description="Convertisseur d'images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  toolbox run image_converter input.jpg output.png
  toolbox run image_converter photo.png photo.webp --quality 80
  toolbox run image_converter --info photo.jpg
        """
    )
    
    parser.add_argument('input', nargs='?', help='Fichier image source')
    parser.add_argument('output', nargs='?', help='Fichier image de destination')
    parser.add_argument('--quality', '-q', type=int, default=95, 
                       help='Qualité de compression (1-100, défaut: 95)')
    parser.add_argument('--info', '-i', action='store_true',
                       help='Affiche les informations de l\'image')
    
    # Parse les arguments
    parsed_args = parser.parse_args(args)
    
    # Mode information
    if parsed_args.info:
        if not parsed_args.input:
            print("Erreur: Spécifiez un fichier image avec --info")
            return 1
        
        if not Path(parsed_args.input).exists():
            print(f"Erreur: Le fichier '{parsed_args.input}' n'existe pas")
            return 1
        
        success = get_image_info(parsed_args.input)
        return 0 if success else 1
    
    # Mode conversion
    if not parsed_args.input or not parsed_args.output:
        print("Erreur: Spécifiez les fichiers d'entrée et de sortie")
        parser.print_help()
        return 1
    
    # Vérifie que le fichier source existe
    if not Path(parsed_args.input).exists():
        print(f"Erreur: Le fichier '{parsed_args.input}' n'existe pas")
        return 1
    
    # Vérifie la qualité
    if not 1 <= parsed_args.quality <= 100:
        print("Erreur: La qualité doit être entre 1 et 100")
        return 1
    
    # Effectue la conversion
    print(f"Conversion de '{parsed_args.input}' vers '{parsed_args.output}'...")
    success = convert_image(parsed_args.input, parsed_args.output, parsed_args.quality)
    
    if success:
        print("Conversion réussie!")
        return 0
    else:
        return 1

# Test direct du module
if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))