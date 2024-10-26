import os
import shutil

def run(source_file):
    modules_dir = os.path.join(os.path.dirname(__file__), '../modules')

    # Vérifer les args
    if not source_file:
        print(f"Missing args")
        return

    # Vérifie si le fichier source existe
    if not os.path.isfile(source_file):
        print(f"Le fichier '{source_file}' n'existe pas.")
        return

    # Vérifie si le répertoire modules existe, sinon le créer
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)

    # Détermine le nom du fichier cible
    module_name = os.path.basename(source_file)
    destination = os.path.join(modules_dir, module_name)

    # Copie le fichier dans le dossier modules
    try:
        shutil.copy(source_file, destination)
        print(f"Module '{module_name}' installé avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'installation du module : {e}")
