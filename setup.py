#!/usr/bin/env python3
"""
Script d'installation pour Toolbox
Installe l'application et configure l'environnement
"""

import os
import sys
import shutil
import platform
from pathlib import Path

def get_install_paths():
    """Détermine les chemins d'installation selon l'OS"""
    system = platform.system().lower()
    
    if system == "windows":
        # Windows
        program_files = Path(os.environ.get('PROGRAMFILES', 'C:/Program Files'))
        install_dir = program_files / "Toolbox"
        bin_dir = install_dir
        
        # Dossier dans PATH pour Windows
        user_scripts = Path(os.environ.get('APPDATA', '')) / "Python" / "Scripts"
        if not user_scripts.exists():
            user_scripts = Path.home() / "AppData" / "Roaming" / "Python" / "Scripts"
        
        return install_dir, user_scripts
    
    elif system == "darwin":
        # macOS  
        install_dir = Path("/usr/local/lib/toolbox")
        bin_dir = Path("/usr/local/bin")
        return install_dir, bin_dir
    
    else:
        # Linux et autres Unix
        install_dir = Path("/opt/toolbox")
        bin_dir = Path("/usr/local/bin")
        return install_dir, bin_dir

def create_launcher_script(install_dir: Path, bin_dir: Path):
    """Crée le script de lancement"""
    system = platform.system().lower()
    
    if system == "windows":
        # Script batch pour Windows
        launcher_content = f"""@echo off
python "{install_dir / 'toolbox.py'}" %*
"""
        launcher_path = bin_dir / "toolbox.bat"
        
        # Script PowerShell alternatif
        ps_content = f"""#!/usr/bin/env pwsh
python "{install_dir / 'toolbox.py'}" $args
"""
        ps_path = bin_dir / "toolbox.ps1"
        
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        with open(ps_path, 'w') as f:
            f.write(ps_content)
        
        return [launcher_path, ps_path]
    
    else:
        # Script shell pour Unix/Linux/macOS
        launcher_content = f"""#!/bin/bash
python3 "{install_dir / 'toolbox.py'}" "$@"
"""
        launcher_path = bin_dir / "toolbox"
        
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        # Rend exécutable
        os.chmod(launcher_path, 0o755)
        
        return [launcher_path]

def install_toolbox():
    """Installation principale"""
    print("=== Installation de Toolbox ===")
    print()
    
    # Vérifie Python
    if sys.version_info < (3, 6):
        print("Erreur: Python 3.6 ou plus récent est requis")
        return False
    
    print(f"Python {sys.version} détecté ✓")
    
    # Détermine les chemins
    install_dir, bin_dir = get_install_paths()
    
    print(f"Répertoire d'installation: {install_dir}")
    print(f"Répertoire des exécutables: {bin_dir}")
    print()
    
    try:
        # Crée les répertoires
        install_dir.mkdir(parents=True, exist_ok=True)
        bin_dir.mkdir(parents=True, exist_ok=True)
        
        # Copie le fichier principal
        script_dir = Path(__file__).parent
        main_script = script_dir / "toolbox.py"
        
        if not main_script.exists():
            print("Erreur: toolbox.py introuvable dans le répertoire actuel")
            return False
        
        shutil.copy2(main_script, install_dir / "toolbox.py")
        print("Fichier principal copié ✓")
        
        # Crée les scripts de lancement
        launchers = create_launcher_script(install_dir, bin_dir)
        print(f"Scripts de lancement créés: {[str(l) for l in launchers]} ✓")
        
        # Installe les modules d'exemple
        examples_dir = script_dir / "modules"
        if examples_dir.exists():
            for module_file in examples_dir.glob("*.py"):
                dest = install_dir / "examples" / module_file.name
                dest.parent.mkdir(exist_ok=True)
                shutil.copy2(module_file, dest)
            print("Modules d'exemple installés ✓")
        
        print()
        print("=== Installation terminée avec succès! ===")
        print()
        print("Pour utiliser Toolbox:")
        print("  toolbox list              # Liste les modules")
        print("  toolbox run <module>      # Exécute un module")
        print("  toolbox install <file>    # Installe un nouveau module")
        print()
        
        # Instructions spécifiques à l'OS
        system = platform.system().lower()
        if system == "windows":
            print("Note Windows:")
            print(f"  - Ajoutez {bin_dir} à votre PATH si nécessaire")
            print("  - Redémarrez votre terminal après installation")
        else:
            print("Note Unix/Linux:")
            print(f"  - {bin_dir} devrait être dans votre PATH")
            print("  - Utilisez 'sudo' si vous avez des erreurs de permissions")
        
        return True
        
    except PermissionError:
        print("Erreur: Permissions insuffisantes")
        if platform.system().lower() != "windows":
            print("Essayez avec: sudo python3 setup.py")
        else:
            print("Exécutez en tant qu'administrateur")
        return False
    
    except Exception as e:
        print(f"Erreur lors de l'installation: {e}")
        return False

def uninstall_toolbox():
    """Désinstallation"""
    print("=== Désinstallation de Toolbox ===")
    
    install_dir, bin_dir = get_install_paths()
    
    try:
        # Supprime le répertoire d'installation
        if install_dir.exists():
            shutil.rmtree(install_dir)
            print(f"Répertoire {install_dir} supprimé ✓")
        
        # Supprime les lanceurs
        system = platform.system().lower()
        if system == "windows":
            for launcher in ["toolbox.bat", "toolbox.ps1"]:
                launcher_path = bin_dir / launcher
                if launcher_path.exists():
                    launcher_path.unlink()
                    print(f"Lanceur {launcher_path} supprimé ✓")
        else:
            launcher_path = bin_dir / "toolbox"
            if launcher_path.exists():
                launcher_path.unlink()
                print(f"Lanceur {launcher_path} supprimé ✓")
        
        print("Désinstallation terminée ✓")
        return True
        
    except Exception as e:
        print(f"Erreur lors de la désinstallation: {e}")
        return False

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        success = uninstall_toolbox()
    else:
        success = install_toolbox()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())