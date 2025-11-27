#!/usr/bin/env python3
"""
Module de téléchargement pour Toolbox
Télécharge des fichiers depuis des URLs
"""

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse

VERSION = "1.0.0"
DESCRIPTION = "Télécharge des fichiers depuis des URLs"

def download_file(url: str, output_path: str = None, show_progress: bool = True):
    """Télécharge un fichier depuis une URL"""
    try:
        import requests
        from tqdm import tqdm
    except ImportError:
        print("Erreur: Les modules 'requests' et 'tqdm' sont requis")
        print("Installez-les avec: pip install requests tqdm")
        return False
    
    try:
        # Détermine le nom de fichier si non spécifié
        if not output_path:
            parsed_url = urlparse(url)
            output_path = Path(parsed_url.path).name
            if not output_path:
                output_path = "downloaded_file"
        
        # Télécharge avec barre de progression
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f:
            if show_progress and total_size > 0:
                with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            else:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        
        print(f"Fichier téléchargé: {output_path}")
        return True
        
    except Exception as e:
        print(f"Erreur lors du téléchargement: {e}")
        return False

def main(args):
    parser = argparse.ArgumentParser(description="Téléchargeur de fichiers")
    parser.add_argument('url', help='URL du fichier à télécharger')
    parser.add_argument('-o', '--output', help='Nom du fichier de sortie')
    parser.add_argument('--no-progress', action='store_true', 
                       help='Désactive la barre de progression')
    
    parsed_args = parser.parse_args(args)
    
    success = download_file(
        parsed_args.url, 
        parsed_args.output, 
        not parsed_args.no_progress
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
