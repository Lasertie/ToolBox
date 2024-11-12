# Couleur : couleur de remplacement (en hexadécimal, ex : #FF5733 ou en tuple RGB, ex : (255, 87, 51))
# File : nom du fichier d'entrée (avec extension)
# Path (facultatif) : chemin absolu vers le fichier d'entrée et de sortie

import os
from PIL import Image

def run(color, file, path=""):
    try:
        # Détermine le chemin du fichier d'entrée et de sortie
        input_file = os.path.join(path, file)
        output_file = os.path.join(path, f"recolor_{file}")

        # Vérifie si le fichier d'entrée existe
        if not os.path.isfile(input_file):
            print(f"Erreur : fichier d'entrée '{input_file}' introuvable.")
            return

        # Ouvre l'image en mode RGBA pour la gestion de la transparence
        with Image.open(input_file).convert("RGBA") as img:
            # Convertit la couleur d'entrée en RGB
            if isinstance(color, str):
                if color.startswith("#"):
                    color = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))  # Convertit hexadécimal en RGB
                else:
                    print("Erreur : spécifiez la couleur en format hexadécimal (ex : #FF5733) ou tuple RGB.")
                    return

            # Applique la nouvelle couleur
            recolored_img = Image.new("RGBA", img.size)
            for x in range(img.width):
                for y in range(img.height):
                    r, g, b, a = img.getpixel((x, y))
                    if a > 0:  # Conserve la transparence de l'image originale
                        recolored_img.putpixel((x, y), (*color, a))

            # Sauvegarde l'image recoloriée
            recolored_img.save(output_file)
            print(f"Image recoloriée sauvegardée en '{output_file}'.")

    except Exception as e:
        print(f"Erreur lors de la recoloration : {e}")
