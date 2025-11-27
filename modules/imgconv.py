#!/usr/bin/env python3
"""
Module de conversion d'images
Convertit des images d'un format à un autre (JPG, PNG, WEBP, etc.)
"""

import os
from pathlib import Path
from PIL import Image
import logging

# Informations du module (requis)
MODULE_INFO = {
    'name': 'image-converter',
    'version': '1.0.0',
    'description': 'Convertit des images d\'un format à un autre',
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
            'name': '--format',
            'help': 'Format de sortie (jpg, png, webp, bmp, etc.)',
            'required': True,
            'type': str
        },
        {
            'name': '--quality',
            'help': 'Qualité pour JPEG (1-100)',
            'required': False,
            'type': int,
            'default': 95
        },
        {
            'name': '--recursive',
            'help': 'Traiter récursivement les sous-dossiers',
            'required': False,
            'type': bool,
            'default': False
        }
    ]
}

# Extensions supportées
SUPPORTED_FORMATS = {
    'jpg': 'JPEG',
    'jpeg': 'JPEG',
    'png': 'PNG',
    'webp': 'WebP',
    'bmp': 'BMP',
    'tiff': 'TIFF',
    'gif': 'GIF'
}

def setup_logging():
    """Configuration du logging pour le module"""
    logger = logging.getLogger('image-converter')
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def convert_image(input_path: Path, output_path: Path, format_name: str, quality: int = 95) -> bool:
    """Convertit une image individuelle"""
    logger = setup_logging()
    
    try:
        # Ouvrir l'image
        with Image.open(input_path) as img:
            # Conversion pour certains formats
            if format_name.upper() == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                # JPEG ne supporte pas la transparence
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Sauvegarder avec les paramètres appropriés
            save_kwargs = {}
            if format_name.upper() == 'JPEG':
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True
            elif format_name.upper() == 'PNG':
                save_kwargs['optimize'] = True
            elif format_name.upper() == 'WEBP':
                save_kwargs['quality'] = quality
                save_kwargs['method'] = 6
            
            img.save(output_path, format=format_name.upper(), **save_kwargs)
            
        logger.info(f"✓ {input_path.name} → {output_path.name}")
        return True
        
    except Exception as e:
        logger.error(f"✗ Erreur lors de la conversion de {input_path.name}: {e}")
        return False

def get_output_path(input_path: Path, output_arg: str, new_format: str) -> Path:
    """Détermine le chemin de sortie basé sur les arguments"""
    if output_arg is None:
        # Même nom, nouveau format
        return input_path.with_suffix(f'.{new_format.lower()}')
    
    output_path = Path(output_arg)
    
    if output_path.is_dir() or (not output_path.exists() and not output_path.suffix):
        # Dossier de destination
        output_path.mkdir(parents=True, exist_ok=True)
        return output_path / f"{input_path.stem}.{new_format.lower()}"
    else:
        # Fichier spécifique
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path

def find_images(path: Path, recursive: bool = False) -> list:
    """Trouve tous les fichiers images dans un chemin"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff', '.gif'}
    images = []
    
    if path.is_file():
        if path.suffix.lower() in image_extensions:
            images.append(path)
    elif path.is_dir():
        pattern = "**/*" if recursive else "*"
        for file_path in path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                images.append(file_path)
    
    return images

def execute(args: dict) -> bool:
    """Fonction principale d'exécution du module (requis)"""
    logger = setup_logging()
    
    # Validation des arguments
    input_path = Path(args['input'])
    output_arg = args.get('output')
    target_format = args['format'].lower()
    quality = args.get('quality', 95)
    recursive = args.get('recursive', False)
    
    # Vérifier le format de sortie
    if target_format not in SUPPORTED_FORMATS:
        logger.error(f"Format non supporté: {target_format}")
        logger.info(f"Formats supportés: {', '.join(SUPPORTED_FORMATS.keys())}")
        return False
    
    # Vérifier l'entrée
    if not input_path.exists():
        logger.error(f"Le fichier ou dossier d'entrée n'existe pas: {input_path}")
        return False
    
    # Vérifier Pillow
    try:
        from PIL import Image
    except ImportError:
        logger.error("La bibliothèque Pillow (PIL) n'est pas installée.")
        logger.info("Installez-la avec: pip install Pillow")
        return False
    
    # Trouver les images à traiter
    images = find_images(input_path, recursive)
    
    if not images:
        logger.warning("Aucune image trouvée à traiter")
        return True
    
    logger.info(f"Conversion de {len(images)} image(s) vers le format {target_format.upper()}")
    
    # Traiter chaque image
    success_count = 0
    format_name = SUPPORTED_FORMATS[target_format]
    
    for image_path in images:
        try:
            output_path = get_output_path(image_path, output_arg, target_format)
            
            if convert_image(image_path, output_path, format_name, quality):
                success_count += 1
                
        except Exception as e:
            logger.error(f"Erreur lors du traitement de {image_path}: {e}")
    
    # Résumé
    logger.info(f"Conversion terminée: {success_count}/{len(images)} images converties")
    
    return success_count == len(images)

# Test du module si exécuté directement
if __name__ == "__main__":
    # Test basique
    test_args = {
        'input': 'test.jpg',
        'format': 'png',
        'quality': 95,
        'recursive': False
    }
    
    print("Test du module de conversion d'images...")
    result = execute(test_args)
    print(f"Résultat: {'Succès' if result else 'Échec'}")