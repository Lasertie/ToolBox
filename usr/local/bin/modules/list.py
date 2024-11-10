import os
import shutil

def run():
    modules_dir = os.path.join(os.path.dirname(__file__), '../modules')

    # Vérifie si le répertoire modules existe, sinon le créer
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)
        return ("No modules")
    
    """Liste les modules disponibles dans le dossier 'modules'."""
    available_modules = [f[:-3] for f in os.listdir(modules_dir) if f.endswith(".py")]
    if available_modules:
        print("Modules disponibles :")
        for module in available_modules:
            if module != "__init__" :
                print(f"  - {module}")
        return "OK"
    else:
        print("Aucun module disponible.")
        return "No modules"