# Ce module convertit une image (PNG, JPG, etc.) en SVG
# Utilisation : toolbox svg <file.png> -f <file-en-svg.svg> -p <path/to/output/files>

import os
import cairosvg  # Nécessite d'installer cairosvg pour la gestion des SVG

def run(input_file, file=None, path="."):
    try:
        # Vérifie si l'extension d'entrée est correcte
        if not input_file.lower().endswith((".png", ".jpg", ".jpeg")):
            print("Erreur : seul les fichiers PNG et JPG sont acceptés.")
            return

        # Détermine le nom de fichier de sortie et le chemin
        output_file = file if file else os.path.splitext(input_file)[0] + ".svg"
        output_path = os.path.join(path, output_file)

        # Vérifie si le fichier d'entrée existe
        if not os.path.isfile(input_file):
            print(f"Erreur : fichier d'entrée '{input_file}' introuvable.")
            return

        # Convertit l'image en SVG
        with open(input_file, "rb") as img_file:
            cairosvg.svg2svg(bytestring=img_file.read(), write_to=output_path)

        print(f"Conversion réussie : fichier SVG enregistré sous '{output_path}'.")

    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")
