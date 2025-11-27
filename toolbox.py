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
    
    def module_exists(self, module_name: str) -> bool:
        """Vérifie si un module existe"""
        module_path = self.modules_dir / f"{module_name}.py"
        return module_path.exists()
    
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
    
    def update_module(self, module_name: str, source_path: str = None):
        """Met à jour un module existant"""
        module_path = self.modules_dir / f"{module_name}.py"
        
        # Vérifie si le module existe
        if not module_path.exists():
            print(f"Erreur: Le module '{module_name}' n'est pas installé")
            print(f"Utilisez 'toolbox install' pour installer un nouveau module")
            return 1
        
        # Si aucun chemin source n'est fourni, utilise celui de la config
        if not source_path:
            config = self.load_config()
            if module_name in config['modules'] and 'source' in config['modules'][module_name]:
                source_path = config['modules'][module_name]['source']
            else:
                print(f"Erreur: Aucune source trouvée pour le module '{module_name}'")
                print(f"Spécifiez le chemin du fichier source: toolbox update {module_name} <file>")
                return 1
        
        source = Path(source_path)
        if not source.exists():
            print(f"Erreur: Le fichier source '{source_path}' n'existe pas")
            return 1
        
        if source.suffix != '.py':
            print("Erreur: Le fichier doit avoir l'extension .py")
            return 1
        
        try:
            # Sauvegarde l'ancienne version
            backup_path = self.modules_dir / f"{module_name}.py.backup"
            with open(module_path, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            
            # Copie la nouvelle version
            with open(source, 'r', encoding='utf-8') as src, \
                 open(module_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            
            print(f"✓ Module '{module_name}' mis à jour avec succès")
            print(f"  Backup sauvegardé: {backup_path}")
            
            # Met à jour la configuration
            config = self.load_config()
            if module_name not in config['modules']:
                config['modules'][module_name] = {}
            
            config['modules'][module_name]['source'] = str(source)
            config['modules'][module_name]['last_update'] = str(Path().cwd())
            self.save_config(config)
            
            # Supprime le backup si tout s'est bien passé
            try:
                backup_path.unlink()
            except:
                pass
            
            return 0
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            
            # Restaure le backup en cas d'erreur
            if backup_path.exists():
                try:
                    with open(backup_path, 'r', encoding='utf-8') as backup, \
                         open(module_path, 'w', encoding='utf-8') as module:
                        module.write(backup.read())
                    print("Module restauré depuis le backup")
                except:
                    print(f"ATTENTION: Impossible de restaurer le backup depuis {backup_path}")
            
            return 1


def main():
    toolbox = ToolboxManager()
    
    # Commandes internes de Toolbox
    INTERNAL_COMMANDS = ['list', 'install', 'uninstall', 'update', 'help']
    
    if len(sys.argv) < 2:
        print("Usage: toolbox <commande|module> [options]")
        print("\nCommandes Toolbox:")
        print("  list                    Liste tous les modules disponibles")
        print("  install <file>          Installe un nouveau module")
        print("  update <module> [file]  Met à jour un module existant")
        print("  uninstall <module>      Désinstalle un module")
        print("  help                    Affiche cette aide")
        print("\nExécution de modules:")
        print("  toolbox <module> [args...]  Exécute directement un module")
        print("\nExemples:")
        print("  toolbox list")
        print("  toolbox qr 'https://example.com' -f output.png")
        print("  toolbox install ./mon_module.py")
        print("  toolbox update qr ./qr_v2.py")
        return 0
    
    command = sys.argv[1]
    
    # Gestion des commandes internes
    if command == 'list':
        toolbox.list_modules()
        return 0
    
    elif command == 'help' or command == '--help' or command == '-h':
        print("Toolbox - Gestionnaire de modules Python")
        print("\nCommandes:")
        print("  list                    Liste tous les modules disponibles")
        print("  install <file>          Installe un nouveau module")
        print("  update <module> [file]  Met à jour un module existant")
        print("  uninstall <module>      Désinstalle un module")
        print("  <module> [args...]      Exécute directement un module")
        print("\nExemples:")
        print("  toolbox list")
        print("  toolbox qr 'Mon texte' -f qr.png")
        print("  toolbox install ./nouveau_module.py")
        print("  toolbox update qr ./qr_v2.py")
        print("  toolbox update qr  # Utilise la source enregistrée")
        print("  toolbox uninstall qr")
        return 0
    
    elif command == 'install':
        if len(sys.argv) < 3:
            print("Erreur: Spécifiez le chemin du fichier à installer")
            print("Usage: toolbox install <file>")
            return 1
        
        source_path = sys.argv[2]
        return toolbox.install_module(source_path)
    
    elif command == 'update':
        if len(sys.argv) < 3:
            print("Erreur: Spécifiez le nom du module à mettre à jour")
            print("Usage: toolbox update <module> [file]")
            return 1
        
        module_name = sys.argv[2]
        source_path = sys.argv[3] if len(sys.argv) > 3 else None
        return toolbox.update_module(module_name, source_path)
    
    elif command == 'uninstall':
        if len(sys.argv) < 3:
            print("Erreur: Spécifiez le nom du module à désinstaller")
            print("Usage: toolbox uninstall <module>")
            return 1
        
        module_name = sys.argv[2]
        return toolbox.uninstall_module(module_name)
    
    # Si ce n'est pas une commande interne, considérer que c'est un module
    else:
        module_name = command
        
        # Vérifier si le module existe
        if not toolbox.module_exists(module_name):
            print(f"Erreur: Module ou commande '{module_name}' introuvable")
            print(f"\nModules disponibles:")
            modules = toolbox.discover_modules()
            if modules:
                for mod in modules:
                    print(f"  - {mod}")
            else:
                print("  (aucun module installé)")
            print(f"\nCommandes disponibles: {', '.join(INTERNAL_COMMANDS)}")
            return 1
        
        # Exécuter le module avec tous les arguments restants
        module_args = sys.argv[2:]
        return toolbox.run_module(module_name, module_args)


if __name__ == "__main__":
    sys.exit(main())