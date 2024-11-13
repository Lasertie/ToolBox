# Ce module convertit une image (PNG, JPG, etc.) en un SVG simple avec contours
# Utilisation : toolbox svg <file.png> -f <file-en-svg.svg> -p <path/to/output/files>

import os
from PIL import Image, ImageOps

def run(input_file, file=None, path="."):
    try:
        # Vérifie l'extension
        if not input_file.lower().endswith((".png", ".jpg", ".jpeg")):
            print("Erreur : seuls les fichiers PNG et JPG sont acceptés.")
            return

        # Définit le nom de fichier de sortie
        output_file = file if file else os.path.splitext(input_file)[0] + ".svg"
        output_path = os.path.join(path, output_file)

        # Vérifie l'existence du fichier d'entrée
        if not os.path.isfile(input_file):
            print(f"Erreur : fichier d'entrée '{input_file}' introuvable.")
            return

        # Charge et convertit l'image en noir et blanc
        with Image.open(input_file) as img:
            img = ImageOps.grayscale(img)
            img = img.point(lambda x: 0 if x < 128 else 255, '1')

        # Création de contours simples en SVG
        width, height = img.size
        svg_content = f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}'>\n"
        pixels = img.load()

        # Parcourt chaque pixel pour générer un carré noir ou blanc
        for y in range(height):
            for x in range(width):
                if pixels[x, y] == 0:
                    svg_content += f"<rect x='{x}' y='{y}' width='1' height='1' fill='black' />\n"

        svg_content += "</svg>"

        # Écrit le contenu SVG dans le fichier de sortie
        with open(output_path, "w") as svg_file:
            svg_file.write(svg_content)

        print(f"Conversion réussie : fichier SVG enregistré sous '{output_path}'.")

    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")
