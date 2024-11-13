# Module pour supprimer le fond d'une image
# Utilisation : toolbox back-rm <file.png> [-f <output.png>] [-p <path/to/output>]

import os
from PIL import Image
from rembg import remove

def run(input_file, file=None, path="."):
    try:
        # Vérifie l'extension de l'image
        if not input_file.lower().endswith((".png", ".jpg", ".jpeg")):
            print("Erreur : seuls les fichiers PNG et JPG sont acceptés.")
            return

        # Définit le nom de fichier de sortie
        output_file = file if file else os.path.splitext(input_file)[0] + "_no_bg.png"
        output_path = os.path.join(path, output_file)

        # Vérifie si le fichier d'entrée existe
        if not os.path.isfile(input_file):
            print(f"Erreur : fichier d'entrée '{input_file}' introuvable.")
            return

        # Chargement de l'image et suppression du fond
        with open(input_file, "rb") as img_file:
            input_data = img_file.read()
            output_data = remove(input_data)

        # Sauvegarde du résultat dans un fichier PNG avec fond transparent
        with open(output_path, "wb") as out_file:
            out_file.write(output_data)

        print(f"Suppression du fond réussie : fichier sauvegardé sous '{output_path}'.")

    except Exception as e:
        print(f"Erreur lors de la suppression du fond : {e}")
