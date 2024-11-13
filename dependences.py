import os
import subprocess
import sys
import venv

def create_and_install_env(requirements_file="requirements.txt", env_dir="env"):
    # Créer un environnement virtuel
    print("Création de l'environnement virtuel...")
    venv.create(env_dir, with_pip=True)
    
    # Définir le chemin de l'exécutable pip dans l'environnement virtuel
    pip_path = os.path.join(env_dir, "bin", "pip") if os.name != 'nt' else os.path.join(env_dir, "Scripts", "pip.exe")
    
    # Installer les dépendances depuis requirements.txt
    if os.path.isfile(requirements_file):
        print(f"Installation des dépendances depuis {requirements_file}...")
        subprocess.check_call([pip_path, "install", "-r", requirements_file])
        print("Installation des dépendances terminée.")
    else:
        print(f"Erreur : Le fichier {requirements_file} est introuvable.")
        sys.exit(1)

    print("L'environnement virtuel est prêt à être utilisé.")

if __name__ == "__main__":
    create_and_install_env()
