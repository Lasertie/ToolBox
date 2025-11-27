#!/usr/bin/env python3
"""
Module de redimensionnement d'images
Redimensionne des images en conservant ou non les proportions
"""

import os
from pathlib import Path
from PIL import Image, ImageFilter
import logging

# Informations du module (requis)
MODULE_INFO = {
    'name': 'image-resizer',
    'version': '1.0.0',
    'description': 'Redimensionne des images avec différentes options',
    'author': 'Assistant',
    'arguments': [
        {
            'name': '--input',
            'help': 'Fichier image d\'entrée ou dossier',
            'required': True,
            'type': str
        },
        {
            'name': '--output',
            'help': 'Fichier de sortie ou dossier de destination',
            'required': False,
            'type': str,
            'default': None
        },
        {
            'name': '--width',
            'help': 'Largeur cible en pixels',
            'required': False,
            'type': int,
            'default': None
        },
        {
            'name': '--height',
            'help': 'Hauteur cible en pixels',
            'required': False,
            'type': int,
            'default': None
        },
        {
            'name': '--scale',
            'help': 'Facteur d\'échelle (ex: 0.5 pour 50%)',
            'required': False,
            'type': float,
            'default': None
        },
        {
            'name': '--keep-aspect',
            'help': 'Conserver les proportions',
            'required': False,
            'type': bool,
            'default': True
        },
        {
            'name': '--quality',
            'help': 'Qualité pour JPEG (1-100)',
            'required': False,
            'type': int,
            'default': 95
        },
        {
            'name': '--method',
            'help': 'Méthode de redimensionnement (lanczos, cubic, linear, nearest)',
            'required': False,
            'type': str,
            'default': 'lanczos'
        }
    ]
}

def setup_logging():
    """Configuration du logging pour le module"""
    logger = logging.getLogger('image-resizer')
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def get_resize_method(method_name: str):
    """Retourne la méthode de redimensionnement PIL"""
    methods = {
        'lanczos': Image.Resampling.LANCZOS,
        'cubic': Image.Resampling.BICUBIC,
        'linear': Image.Resampling.BILINEAR,
        'nearest': Image.Resampling.NEAREST
    }
    return methods.get(method_name.lower(), Image.Resampling.LANCZOS)

def calculate_dimensions(original_size, target_width, target_height, scale, keep_aspect):
    """Calcule les nouvelles dimensions selon les paramètres"""
    orig_width, orig_height = original_size
    
    # Si un facteur d'échelle est spécifié
    if scale is not None:
        return int(orig_width * scale), int(orig_height * scale)
    
    # Si ni largeur ni hauteur spécifiées
    if target_width is None and target_height is None:
        return orig_width, orig_height
    
    # Si les deux dimensions sont spécifiées
    if target_width is not None and target_height is not None:
        if not keep_aspect:
            return target_width, target_height
        else:
            # Garder les proportions, utiliser la dimension qui crée le plus petit redimensionnement
            scale_w = target_width / orig_width
            scale_h = target_height / orig_height
            scale_factor = min(scale_w, scale_h)
            return int(orig_width * scale_factor), int(orig_height * scale_factor)
    
    # Si seule la largeur est spécifiée
    if target_width is not None:
        if keep_aspect:
            scale_factor = target_width / orig_width
            return target_width, int(orig_height * scale_factor)
        else:
            return target_width, orig_height
    
    # Si seule la hauteur est spécifiée
    if target_height is not None:
        if keep_aspect:
            scale_factor = target_height / orig_height
            return int(orig_width * scale_factor), target_height
        else:
            return orig_width, target_height

def resize_image(input_path: Path, output_path: Path, new_size: tuple, method, quality: int = 95) -> bool:
    """Redimensionne une image individuelle"""
    logger = setup_logging()
    
    try:
        with Image.open(input_path) as img:
            # Redimensionner
            resized_img = img.resize(new_size, method)
            
            # Préparer les paramètres de sauvegarde
            save_kwargs = {}
            if output_path.suffix.lower() in ['.jpg', '.jpeg']:
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True
                # Convertir en RGB si nécessaire pour JPEG
                if resized_img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', resized_img.size, (255, 255, 255))
                    if resized_img.mode == 'P':
                        resized_img = resized_img.convert('RGBA')
                    background.paste(resized_img, mask=resized_img.split()[-1] if resized_img.mode == 'RGBA' else None)
                    resized_img = background
            elif output_path.suffix.lower() == '.png':
                save_kwargs['optimize'] = True
            
            # Sauvegarder
            resized_img.save(output_path, **save_kwargs)
            
            # Informations sur le redimensionnement
            orig_size = img.size
            logger.info(f"✓ {input_path.name}: {orig_size[0]}x{orig_size[1]} → {new_size[0]}x{new_size[1]}")
            return True
            
    except Exception as e:
        logger.error(f"✗ Erreur lors du redimensionnement de {input_path.name}: {e}")
        return False

def get_output_path(input_path: Path, output_arg: str) -> Path:
    """Détermine le chemin de sortie"""
    if output_arg is None:
        # Même emplacement, ajouter suffix
        return input_path.with_stem(f"{input_path.stem}_resized")
    
    output_path = Path(output_arg)
    
    if output_path.is_dir() or (not output_path.exists() and not output_path.suffix):
        # Dossier de destination
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path / input_path.name
    else:
        # Fichier spécifique
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path

def find_images(path: Path) -> list:
    """Trouve tous les fichiers images dans un chemin"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.gif'}
    images = []
    
    if path.is_file():
        if path.suffix.lower() in image_extensions:
            images.append(path)
    elif path.is_dir():
        for file_path in path.glob("*"):
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                images.append(file_path)
    
    return images

def execute(args: dict) -> bool:
    """Fonction principale d'exécution du module (requis)"""
    logger = setup_logging()
    
    # Validation des arguments
    input_path = Path(args['input'])
    output_arg = args.get('output')
    target_width = args.get('width')
    target_height = args.get('height')
    scale = args.get('scale')
    keep_aspect = args.get('keep_aspect', True)
    quality = args.get('quality', 95)
    method_name = args.get('method', 'lanczos')
    
    # Vérifier l'entrée
    if not input_path.exists():
        logger.error(f"Le fichier ou dossier d'entrée n'existe pas: {input_path}")
        return False
    
    # Vérifier qu'au moins un paramètre de redimensionnement est fourni
    if target_width is None and target_height is None and scale is None:
        logger.error("Au moins un paramètre de redimensionnement doit être spécifié (--width, --height, ou --scale)")
        return False
    
    # Vérifier Pillow
    try:
        from PIL import Image
    except ImportError:
        logger.error("La bibliothèque Pillow (PIL) n'est pas installée.")
        logger.info("Installez-la avec: pip install Pillow")
        return False
    
    # Obtenir la méthode de redimensionnement
    resize_method = get_resize_method(method_name)
    
    # Trouver les images à traiter
    images = find_images(input_path)
    
    if not images:
        logger.warning("Aucune image trouvée à traiter")
        return True
    
    logger.info(f"Redimensionnement de {len(images)} image(s)")
    
    # Traiter chaque image
    success_count = 0
    
    for image_path in images:
        try:
            # Obtenir les dimensions originales
            with Image.open(image_path) as img:
                original_size = img.size
            
            # Calculer les nouvelles dimensions
            new_size = calculate_dimensions(
                original_size, target_width, target_height, scale, keep_aspect
            )
            
            # Éviter le redimensionnement inutile
            if new_size == original_size:
                logger.info(f"⚠ {image_path.name}: Aucun redimensionnement nécessaire")
                continue
            
            # Déterminer le chemin de sortie
            output_path = get_output_path(image_path, output_arg)
            
            if resize_image(image_path, output_path, new_size, resize_method, quality):
                success_count += 1
                
        except Exception as e:
            logger.error(f"Erreur lors du traitement de {image_path}: {e}")
    
    # Résumé
    logger.info(f"Redimensionnement terminé: {success_count}/{len(images)} images traitées")
    
    return success_count > 0

# Test du module si exécuté directement
if __name__ == "__main__":
    # Test basique
    test_args = {
        'input': 'test.jpg',
        'width': 800,
        'keep_aspect': True,
        'quality': 95,
        'method': 'lanczos'
    }
    
    print("Test du module de redimensionnement d'images...")
    result = execute(test_args)
    print(f"Résultat: {'Succès' if result else 'Échec'}")