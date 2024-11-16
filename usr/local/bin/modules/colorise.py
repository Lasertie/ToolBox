"""
Module : colorise
Description :
    Ce module permet de recolorer une image tout en conservant sa transparence. 
    La nouvelle couleur est appliquée à tous les pixels visibles de l'image, tandis que les zones transparentes restent inchangées.

Utilisation :
    toolbox colorise <couleur> <fichier> [-p <chemin>] [-h]

Arguments :
    <couleur>   : Couleur de remplacement pour l'image. 
                  Doit être au format hexadécimal (ex : #FF5733) ou en tuple RGB (ex : (255, 87, 51)).
    <fichier>   : Nom ou chemin du fichier d'entrée à recolorer (ex : image.png).
    -p <chemin> : (Optionnel) Chemin absolu vers le répertoire contenant le fichier d'entrée et de sortie.
                  Si non spécifié, le chemin sera extrait du fichier d'entrée ou le répertoire courant sera utilisé.
    -h          : Affiche l'aide pour le module.

Exemples :
    1. Recolorer une image avec une couleur hexadécimale dans le répertoire courant :
        toolbox colorise "#FF5733" image.png
    
    2. Recolorer une image en spécifiant un chemin d'entrée et de sortie :
        toolbox colorise "#87CEEB" /home/user/images/image.png

    3. Recolorer une image et spécifier un chemin séparément :
        toolbox colorise "#228B22" image.png -p /home/user/images

Sortie :
    - L'image recoloriée sera enregistrée avec le préfixe `recolor_` dans le même répertoire que l'image d'entrée ou dans le chemin spécifié.
    - En cas d'erreur, un message descriptif sera affiché dans le terminal.

Remarques :
    - Les images doivent être au format compatible avec la bibliothèque Pillow (PNG, JPEG, etc.).
    - Les zones transparentes de l'image d'entrée ne seront pas recolorées.

Dépendances :
    - Pillow : Une bibliothèque Python pour le traitement des images (peut être installée avec `pip install pillow`).
"""


# Couleur : couleur de remplacement (en hexadécimal, ex : #FF5733 ou en tuple RGB, ex : (255, 87, 51))
# File : nom du fichier d'entrée (avec extension)
# Path (facultatif) : chemin absolu vers le fichier d'entrée et de sortie

import os
from PIL import Image

def run(color, file, path=""):
    try:
        # Separation du path si il existe
        if os.path.dirname(file):
            in_path, file = os.path.split(file)
        # Détermine le chemin du fichier d'entrée et de sortie
        input_file = os.path.join(in_path, file)
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

