import qrcode
import base64
from io import BytesIO
import os
import sys

def run(data, file=None, path=None):
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
        # Si un chemin est précisé, l'utilise, sinon, enregistre dans le répertoire courant
        if path:
            full_path = os.path.join(path, file)
        else:
            full_path = file
        
        # Sauvegarde l'image sous forme de fichier PNG
        qr.save(full_path)
        print(f"QR code saved at {full_path}")
    
    # Retourne la représentation en base64 du QR code
    return qr_base64
