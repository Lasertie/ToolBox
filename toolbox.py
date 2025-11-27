#!/usr/bin/env python3
"""
Toolbox - Application modulaire en ligne de commande
Permet d'exécuter des modules Python interchangeables
"""

import os
import sys
import argparse
import importlib.util
import json
from pathlib import Path
from typing import Dict, List, Any

class ToolboxManager:
    def __init__(self):
        self.toolbox_dir = Path.home() / ".toolbox"
        self.modules_dir = self.toolbox_dir / "modules"
        self.config_file = self.toolbox_dir / "config.json"
        self.ensure_directories()
        
    def ensure_directories(self):
        """Crée les répertoires nécessaires s'ils n'existent pas"""
        self.toolbox_dir.mkdir(exist_ok=True)
        self.modules_dir.mkdir(exist_ok=True)
        
        # Crée un fichier de configuration par défaut
        if not self.config_file.exists():
            default_config = {
                "version": "1.0.0",
                "modules": {}
            }
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
    
    def load_config(self) -> Dict[str, Any]:
        """Charge la configuration"""
        with open(self.config_file, 'r') as f:
            return json.load(f)
    
    def save_config(self, config: Dict[str, Any]):
        """Sauvegarde la configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def discover_modules(self) -> List[str]:
        """Découvre tous les modules disponibles"""
        modules = []
        for file_path in self.modules_dir.glob("*.py"):
            if not file_path.name.startswith("__"):
                modules.append(file_path.stem)
        return sorted(modules)
    
    def load_module(self, module_name: str):
        """Charge un module spécifique"""
        module_path = self.modules_dir / f"{module_name}.py"
        if not module_path.exists():
            raise FileNotFoundError(f"Module '{module_name}' introuvable")
        
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    def list_modules(self):
        """Liste tous les modules disponibles"""
        modules = self.discover_modules()
        if not modules:
            print("Aucun module installé.")
            print(f"Ajoutez vos modules dans: {self.modules_dir}")
            return
        
        print("Modules disponibles:")
        print("-" * 40)
        
        for module_name in modules:
            try:
                module = self.load_module(module_name)
                description = getattr(module, 'DESCRIPTION', 'Aucune description')
                version = getattr(module, 'VERSION', '1.0.0')
                print(f"  {module_name:<15} - {description} (v{version})")
            except Exception as e:
                print(f"  {module_name:<15} - Erreur de chargement: {str(e)}")
    
    def run_module(self, module_name: str, args: List[str]):
        """Exécute un module avec ses arguments"""
        try:
            module = self.load_module(module_name)
            
            # Vérifie si le module a une fonction main
            if not hasattr(module, 'main'):
                raise AttributeError(f"Le module '{module_name}' n'a pas de fonction 'main()'")
            
            # Exécute le module
            return module.main(args)
            
        except FileNotFoundError as e:
            print(f"Erreur: {e}")
            return 1
        except Exception as e:
            print(f"Erreur lors de l'exécution du module '{module_name}': {e}")
            return 1
    
    def install_module(self, source_path: str):
        """Installe un nouveau module"""
        source = Path(source_path)
        if not source.exists():
            print(f"Erreur: Le fichier '{source_path}' n'existe pas")
            return 1
        
        if source.suffix != '.py':
            print("Erreur: Le fichier doit avoir l'extension .py")
            return 1
        
        dest = self.modules_dir / source.name
        
        try:
            # Copie le fichier
            with open(source, 'r', encoding='utf-8') as src, \
                 open(dest, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            
            print(f"Module '{source.stem}' installé avec succès")
            
            # Met à jour la configuration
            config = self.load_config()
            config['modules'][source.stem] = {
                'installed_date': str(Path().cwd()),
                'source': str(source)
            }
            self.save_config(config)
            
            return 0
        except Exception as e:
            print(f"Erreur lors de l'installation: {e}")
            return 1
    
    def uninstall_module(self, module_name: str):
        """Désinstalle un module"""
        module_path = self.modules_dir / f"{module_name}.py"
        
        if not module_path.exists():
            print(f"Erreur: Le module '{module_name}' n'est pas installé")
            return 1
        
        try:
            module_path.unlink()
            print(f"Module '{module_name}' désinstallé avec succès")
            
            # Met à jour la configuration
            config = self.load_config()
            if module_name in config['modules']:
                del config['modules'][module_name]
                self.save_config(config)
            
            return 0
        except Exception as e:
            print(f"Erreur lors de la désinstallation: {e}")
            return 1


def main():
    parser = argparse.ArgumentParser(
        description="Toolbox - Gestionnaire de modules Python",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  toolbox list                    # Liste tous les modules
  toolbox run image_converter input.jpg output.png  # Exécute un module
  toolbox install ./mon_module.py # Installe un nouveau module
  toolbox uninstall image_converter # Désinstalle un module
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
    
    # Commande list
    subparsers.add_parser('list', help='Liste tous les modules disponibles')
    
    # Commande run
    run_parser = subparsers.add_parser('run', help='Exécute un module')
    run_parser.add_argument('module', help='Nom du module à exécuter')
    run_parser.add_argument('args', nargs='*', help='Arguments pour le module')
    
    # Commande install
    install_parser = subparsers.add_parser('install', help='Installe un nouveau module')
    install_parser.add_argument('source', help='Chemin vers le fichier Python à installer')
    
    # Commande uninstall
    uninstall_parser = subparsers.add_parser('uninstall', help='Désinstalle un module')
    uninstall_parser.add_argument('module', help='Nom du module à désinstaller')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    toolbox = ToolboxManager()
    
    if args.command == 'list':
        toolbox.list_modules()
        return 0
    
    elif args.command == 'run':
        return toolbox.run_module(args.module, args.args)
    
    elif args.command == 'install':
        return toolbox.install_module(args.source)
    
    elif args.command == 'uninstall':
        return toolbox.uninstall_module(args.module)


if __name__ == "__main__":
    sys.exit(main())