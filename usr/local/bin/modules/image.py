# Format : format_input-format_output ex: png-svg
# File : nom du fichier à convertir (avec extension d'entrée)
# Path (facultatif) : chemin absolu du dossier contenant le fichier d'entrée et de sortie

import os
from PIL import Image  # Nécessite d'installer Pillow pour la gestion d'images

def run(format, file, path=""):
    try:
        # Vérifie si les formats sont indiqués sous forme format_input-format_output
        if '-' not in format:
            print("Erreur : spécifiez le format sous la forme 'format_input-format_output' (ex: png-svg).")
            return
        format_input, format_output = format.split('-')
        
        # Vérifie si le fichier possède l'extension d'entrée attendue
        if not file.endswith(f".{format_input}"):
            print(f"Erreur : le fichier '{file}' n'a pas l'extension attendue '.{format_input}'.")
            return
        
        # Détermine les chemins de fichier d'entrée et de sortie
        input_file = os.path.join(path, file)
        output_file = os.path.join(path, f"{os.path.splitext(file)[0]}.{format_output}")

        # Vérifie si le fichier d'entrée existe
        if not os.path.isfile(input_file):
            print(f"Erreur : fichier d'entrée '{input_file}' introuvable.")
            return

        # Ouvre le fichier d'entrée et convertit au format de sortie
        with Image.open(input_file) as img:
            img.save(output_file)
        
        print(f"Fichier converti avec succès en '{output_file}'.")

    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")
