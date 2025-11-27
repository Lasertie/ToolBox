#!/usr/bin/env python3
"""
Application CLI Modulaire
Une application en ligne de commande permettant d'utiliser des modules Python interchangeables
pour effectuer diverses opérations (conversion d'images, traitement de fichiers, etc.)
"""

import os
import sys
import json
import argparse
import importlib.util
from pathlib import Path
from typing import Dict, List, Any
import logging

class ModuleManager:
    """Gestionnaire des modules de l'application"""
    
    def __init__(self, modules_dir: str = "modules"):
        self.modules_dir = Path(modules_dir)
        self.modules_dir.mkdir(exist_ok=True)
        self.loaded_modules = {}
        self.setup_logging()
    
    def setup_logging(self):
        """Configuration du logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def discover_modules(self) -> Dict[str, Dict]:
        """Découvre tous les modules disponibles"""
        modules = {}
        
        for module_file in self.modules_dir.glob("*.py"):
            if module_file.name.startswith("_"):
                continue
                
            try:
                module_info = self.load_module_info(module_file)
                if module_info:
                    modules[module_file.stem] = module_info
            except Exception as e:
                self.logger.warning(f"Erreur lors du chargement du module {module_file}: {e}")
        
        return modules
    
    def load_module_info(self, module_file: Path) -> Dict:
        """Charge les informations d'un module"""
        spec = importlib.util.spec_from_file_location(module_file.stem, module_file)
        if spec is None or spec.loader is None:
            return None
            
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Vérification que le module a les attributs requis
        required_attrs = ['MODULE_INFO', 'execute']
        for attr in required_attrs:
            if not hasattr(module, attr):
                raise AttributeError(f"Le module {module_file.stem} doit avoir l'attribut {attr}")
        
        info = module.MODULE_INFO.copy()
        info['module'] = module
        info['file_path'] = str(module_file)
        
        return info
    
    def execute_module(self, module_name: str, args: List[str]) -> bool:
        """Exécute un module avec les arguments donnés"""
        modules = self.discover_modules()
        
        if module_name not in modules:
            self.logger.error(f"Module '{module_name}' non trouvé")
            return False
        
        module_info = modules[module_name]
        
        try:
            # Préparer les arguments pour le module
            module_args = self.parse_module_args(module_info, args)
            
            # Exécuter le module
            result = module_info['module'].execute(module_args)
            
            if result:
                self.logger.info(f"Module '{module_name}' exécuté avec succès")
            else:
                self.logger.error(f"Erreur lors de l'exécution du module '{module_name}'")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution du module '{module_name}': {e}")
            return False
    
    def parse_module_args(self, module_info: Dict, args: List[str]) -> Dict:
        """Parse les arguments pour un module spécifique"""
        parser = argparse.ArgumentParser(
            description=module_info.get('description', ''),
            prog=f"toolbox {module_info['name']}"
        )
        
        # Ajouter les arguments définis par le module
        for arg in module_info.get('arguments', []):
            parser.add_argument(
                arg['name'],
                help=arg.get('help', ''),
                type=arg.get('type', str),
                required=arg.get('required', False),
                default=arg.get('default', None)
            )
        
        return vars(parser.parse_args(args))
    
    def list_modules(self):
        """Liste tous les modules disponibles"""
        modules = self.discover_modules()
        
        if not modules:
            print("Aucun module disponible.")
            return
        
        print("Modules disponibles:")
        print("-" * 50)
        
        for name, info in modules.items():
            print(f"• {name}")
            print(f"  Description: {info.get('description', 'Aucune description')}")
            print(f"  Version: {info.get('version', '1.0.0')}")
            print(f"  Auteur: {info.get('author', 'Inconnu')}")
            
            if info.get('arguments'):
                print("  Arguments:")
                for arg in info['arguments']:
                    required = " (requis)" if arg.get('required') else ""
                    print(f"    {arg['name']}: {arg.get('help', '')}{required}")
            
            print()

class ModularCLI:
    """Application CLI principale"""
    
    def __init__(self):
        self.module_manager = ModuleManager()
    
    def create_parser(self):
        """Crée le parser principal"""
        parser = argparse.ArgumentParser(
            description="Application CLI modulaire pour scripts Python",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Commandes disponibles')
        
        # Commande list
        list_parser = subparsers.add_parser('list', help='Liste tous les modules disponibles')
        
        # Commande run
        run_parser = subparsers.add_parser('run', help='Exécute un module')
        run_parser.add_argument('module', help='Nom du module à exécuter')
        run_parser.add_argument('args', nargs='*', help='Arguments pour le module')
        
        # Commande install
        install_parser = subparsers.add_parser('install', help='Installe un nouveau module')
        install_parser.add_argument('module_file', help='Chemin vers le fichier du module')
        
        return parser
    
    def install_module(self, module_file: str) -> bool:
        """Installe un nouveau module"""
        source_path = Path(module_file)
        
        if not source_path.exists():
            print(f"Erreur: Le fichier {module_file} n'existe pas")
            return False
        
        if not source_path.suffix == '.py':
            print("Erreur: Le fichier doit être un script Python (.py)")
            return False
        
        # Vérifier que le module est valide
        try:
            spec = importlib.util.spec_from_file_location(source_path.stem, source_path)
            if spec is None or spec.loader is None:
                raise ImportError("Impossible de charger le module")
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if not hasattr(module, 'MODULE_INFO'):
                raise AttributeError("Le module doit avoir un attribut MODULE_INFO")
            
            if not hasattr(module, 'execute'):
                raise AttributeError("Le module doit avoir une fonction execute")
        
        except Exception as e:
            print(f"Erreur: Module invalide - {e}")
            return False
        
        # Copier le module
        dest_path = self.module_manager.modules_dir / source_path.name
        
        try:
            import shutil
            shutil.copy2(source_path, dest_path)
            print(f"Module '{source_path.stem}' installé avec succès")
            return True
        except Exception as e:
            print(f"Erreur lors de l'installation: {e}")
            return False
    
    def run(self):
        """Exécute l'application"""
        parser = self.create_parser()
        
        if len(sys.argv) == 1:
            parser.print_help()
            return
        
        args = parser.parse_args()
        
        if args.command == 'list':
            self.module_manager.list_modules()
        
        elif args.command == 'run':
            if not args.module:
                print("Erreur: Nom du module requis")
                return
            
            success = self.module_manager.execute_module(args.module, args.args)
            sys.exit(0 if success else 1)
        
        elif args.command == 'install':
            success = self.install_module(args.module_file)
            sys.exit(0 if success else 1)
        
        else:
            parser.print_help()

def main():
    """Point d'entrée principal"""
    try:
        app = ModularCLI()
        app.run()
    except KeyboardInterrupt:
        print("\nOpération annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()