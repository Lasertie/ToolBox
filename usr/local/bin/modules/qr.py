import qrcode
import base64
from io import BytesIO
import os
import sys

def run(data, file=None, path=None):
    if not data:
        print("Erreur : Les données à encoder dans le QR code ne peuvent pas être vides.")
        return

    try:
        # Génère le QR code
        qr = qrcode.make(data)
        
        # Convertit le QR code en base64 pour l'afficher dans le terminal
        buffered = BytesIO()
        qr.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # Affiche le QR code dans le terminal en utilisant le protocole base64 d'affichage
        sys.stdout.write(f"\033]1337;File=inline=1;width=auto;height=auto;preserveAspectRatio=1:{qr_base64}\a\n")

        # Enregistre le QR code dans un fichier si le paramètre 'file' est défini
        if file:
            if path:
                # Crée le répertoire s'il n'existe pas
                os.makedirs(path, exist_ok=True)
                full_path = os.path.join(path, file)
            else:
                full_path = file

            # Sauvegarde l'image sous forme de fichier PNG
            qr.save(full_path)
            print(f"QR code enregistré à l'emplacement : {full_path}")
        
        # Retourne la représentation en base64 du QR code
        return qr_base64

    except Exception as e:
        print(f"Erreur lors de la génération ou de l'enregistrement du QR code : {e}")
