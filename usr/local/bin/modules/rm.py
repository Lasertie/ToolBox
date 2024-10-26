import os

def run(module_name):
    modules_dir = os.path.join(os.path.dirname(__file__), '../modules')

    # Détermine le chemin complet du module à supprimer
    module_file = os.path.join(modules_dir, f"{module_name}.py")

    if not module_name:
        print(f"Missing args")

    # Vérifie si le fichier existe
    if not os.path.isfile(module_file):
        print(f"Le module '{module_name}' n'existe pas dans le dossier modules.")
        return

    # Supprime le fichier du module
    try:
        os.remove(module_file)
        print(f"Module '{module_name}' supprimé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression du module : {e}")
