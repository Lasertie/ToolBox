#!/usr/bin/env python3
"""
Module QR Code pour Toolbox
Génère des QR codes à partir de données textuelles
"""

import qrcode
import base64
from io import BytesIO
import os
import sys
import argparse

VERSION = "1.2.1"
DESCRIPTION = "Générateur de QR Code"
AUTHOR = "Lasertie"


def generate_qr_code(data, version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, border=4):
    """
    Génère un QR code avec les paramètres spécifiés.
    
    Args:
        data (str): Données à encoder dans le QR code.
        version (int): Version du QR code (de 1 à 40, ou None pour la version par défaut).
        error_correction (int): Niveau de correction d'erreur.
        border (int): Largeur de la bordure (en modules).
    
    Returns:
        PIL.Image: L'image du QR code généré.
    """
    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=10,
        border=border
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


def display_qr_code_ascii(data, error_correction=qrcode.constants.ERROR_CORRECT_L, border=1):
    """Affiche le QR code en ASCII dans le terminal"""
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction,
        box_size=1,
        border=border
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Affiche en utilisant des caractères Unicode
    print()
    matrix = qr.get_matrix()
    
    # Utilise des blocs Unicode pour un meilleur rendu
    for i in range(0, len(matrix), 2):
        line = ""
        for j in range(len(matrix[0])):
            top = matrix[i][j] if i < len(matrix) else False
            bottom = matrix[i+1][j] if i+1 < len(matrix) else False
            
            if top and bottom:
                line += "█"  # Bloc plein
            elif top:
                line += "▀"  # Demi-bloc haut
            elif bottom:
                line += "▄"  # Demi-bloc bas
            else:
                line += " "  # Espace
        print(line)
    print()


def get_error_correction_level(level_str):
    """Convertit une chaîne de caractères en niveau de correction d'erreur."""
    levels = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H
    }
    return levels.get(level_str.upper(), qrcode.constants.ERROR_CORRECT_L)


def main(args):
    """
    Point d'entrée principal pour Toolbox.
    
    Args:
        args (list): Liste des arguments de ligne de commande
    
    Returns:
        int: Code de retour (0 = succès, 1 = erreur)
    """
    parser = argparse.ArgumentParser(
        description=f"{DESCRIPTION} - v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Exemples d'utilisation:
  toolbox qr "https://example.com"
  toolbox qr "Texte du QR code" -f qrcode.png
  toolbox qr "https://example.com" -f output.png -p ./qrcodes
  toolbox qr "Données importantes" -e H -b 2

Auteur: {AUTHOR}
        """
    )
    
    parser.add_argument('data', help='Données à encoder dans le QR code')
    parser.add_argument('-f', '--file', help='Nom du fichier de sortie (PNG)')
    parser.add_argument('-p', '--path', help='Chemin du répertoire de sortie')
    parser.add_argument('-v', '--version', type=int, 
                       help='Version du QR code (1-40, défaut: auto)')
    parser.add_argument('-e', '--error', default='L', 
                       choices=['L', 'M', 'Q', 'H'],
                       help='Niveau de correction d\'erreur (défaut: L)')
    parser.add_argument('-b', '--border', type=int, default=4,
                       help='Largeur de la bordure en modules (défaut: 4)')
    parser.add_argument('--no-display', action='store_true',
                       help='Ne pas afficher le QR code dans le terminal')
    
    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return 1
    
    # Validation des données
    if not parsed_args.data or parsed_args.data.strip() == "":
        print("Erreur : Les données à encoder ne peuvent pas être vides.")
        return 1
    
    try:
        # Obtient le niveau de correction d'erreur
        error_correction = get_error_correction_level(parsed_args.error)
        
        # Affiche le QR code dans le terminal (si demandé)
        if not parsed_args.no_display:
            print(f"QR Code pour : {parsed_args.data[:50]}{'...' if len(parsed_args.data) > 50 else ''}")
            display_qr_code_ascii(parsed_args.data, error_correction, border=1)
        
        # Génère et enregistre le QR code dans un fichier si demandé
        if parsed_args.file:
            qr_image = generate_qr_code(
                parsed_args.data,
                version=parsed_args.version,
                error_correction=error_correction,
                border=parsed_args.border
            )
            
            if parsed_args.path:
                # Crée le répertoire s'il n'existe pas
                os.makedirs(parsed_args.path, exist_ok=True)
                full_path = os.path.join(parsed_args.path, parsed_args.file)
            else:
                full_path = parsed_args.file
            
            # Sauvegarde l'image
            qr_image.save(full_path)
            print(f"✓ QR code enregistré : {full_path}")
        
        return 0
        
    except Exception as e:
        print(f"Erreur lors de la génération du QR code : {e}")
        return 1


if __name__ == "__main__":
    # Test direct du module
    sys.exit(main(sys.argv[1:]))