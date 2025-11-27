![Toolbox](Logo/white_Logo.png)

# Toolbox - Gestionnaire de modules Python

## Description

Toolbox est une application en ligne de commande modulaire qui permet d'exécuter des scripts Python comme des modules interchangeables. L'idée est de pouvoir réaliser en local toutes les opérations que proposent les sites web (conversion d'images, manipulation de fichiers, etc.).

## Fonctionnalités

- **Modulaire** : Ajoutez et supprimez des modules à volonté
- **Multi-plateforme** : Compatible Linux, macOS et Windows
- **Simple** : Interface en ligne de commande intuitive
- **Extensible** : Créez vos propres modules facilement

## Installation

### Prérequis

- Python 3.6 ou plus récent
- pip (gestionnaire de paquets Python)

### Installation automatique

1. Téléchargez tous les fichiers du projet
2. Ouvrez un terminal dans le dossier du projet
3. Exécutez le script d'installation :

**Linux/macOS :**
```bash
sudo python3 setup.py
```

**Windows (en tant qu'administrateur) :**
```cmd
python setup.py
```

### Installation manuelle

1. Créez le dossier d'installation :
   - Linux/macOS : `/opt/toolbox`
   - Windows : `C:\Program Files\Toolbox`

2. Copiez `toolbox.py` dans ce dossier

3. Créez un script de lancement dans votre PATH :
   - Linux/macOS : `/usr/local/bin/toolbox`
   - Windows : Ajoutez le dossier à votre PATH

## Utilisation

### Commandes de base

```bash
# Lister tous les modules disponibles
toolbox list

# Exécuter un module
toolbox <nom_module> [arguments]

# Installer un nouveau module
toolbox install chemin/vers/module.py

# Désinstaller un module
toolbox uninstall nom_module
```

### Exemples

```bash
# Convertir une image JPG en PNG
toolbox run imgconv photo.jpg photo.png

# Convertir avec qualité spécifique
toolbox run imgconv photo.jpg photo.webp --quality 80

# Voir les informations d'une image
toolbox run imgconv --info photo.jpg
```

## Création de modules

### Structure d'un module

Un module Toolbox est un fichier Python avec :

1. **Métadonnées** (optionnelles) :
```python
VERSION = "1.0.0"
DESCRIPTION = "Description du module"
AUTHOR = "Votre nom"
```

2. **Fonction main** (obligatoire) :
```python
def main(args):
    """
    Point d'entrée du module
    
    Args:
        args: Liste des arguments de la ligne de commande
    
    Returns:
        int: Code de retour (0 = succès, autre = erreur)
    """
    # Votre code ici
    return 0
```

### Exemple de module simple

```python
#!/usr/bin/env python3
"""Module exemple pour Toolbox"""

VERSION = "1.0.0"
DESCRIPTION = "Module de démonstration"

def main(args):
    if not args:
        print("Hello, Toolbox!")
    else:
        print(f"Arguments reçus: {' '.join(args)}")
    return 0

# Test direct du module
if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
```

### Bonnes pratiques

1. **Gestion des arguments** : Utilisez `argparse` pour analyser les arguments
2. **Gestion d'erreurs** : Capturez les exceptions et retournez des codes d'erreur appropriés
3. **Documentation** : Incluez une aide accessible via `--help`
4. **Dépendances** : Vérifiez la présence des modules requis et affichez des messages clairs
5. **Tests** : Permettez l'exécution directe du module pour les tests

## Modules inclus

### imgconv

Convertit les images entre différents formats (JPG, PNG, WEBP, BMP).

**Dépendances :**
```bash
pip install Pillow
```

**Usage :**
```bash
# Conversion simple
toolbox run imgconv input.jpg output.png

# Avec qualité personnalisée
toolbox run imgconv input.jpg output.webp --quality 85

# Informations sur une image
toolbox run imgconv --info image.jpg
```

## Structure des fichiers

```
toolbox/
├── toolbox.py              # Application principale
├── setup.py               # Script d'installation
├── README.md              # Cette documentation
├── requirements.txt       # Dépendances Python
└── modules/               # Modules d'exemple
    └── imgconv.py # Convertisseur d'images
```

## Désinstallation

```bash
# Linux/macOS
sudo python3 setup.py uninstall

# Windows (en tant qu'administrateur)
python setup.py uninstall
```

## Développement

### Contribuer

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité
3. Ajoutez vos modifications
4. Testez vos changements
5. Soumettez une pull request

### Créer de nouveaux modules

1. Créez un fichier `.py` avec la structure requise
2. Testez votre module individuellement
3. Installez-le avec `toolbox install`
4. Partagez-le avec la communauté

## Dépannage

### Erreurs courantes

**"Module not found"**
- Vérifiez que le module est installé avec `toolbox list`
- Réinstallez le module si nécessaire

**"Permission denied"**
- Utilisez `sudo` sur Linux/macOS
- Exécutez en tant qu'administrateur sur Windows

**"Python module not found"**
- Installez les dépendances requises avec `pip install`

### Configuration

Les fichiers de configuration se trouvent dans :
- Linux/macOS : `~/.toolbox/`
- Windows : `%USERPROFILE%\.toolbox\`

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Support

Pour obtenir de l'aide :

- Consultez cette documentation
- Vérifiez les exemples de modules
- Ouvrez une issue sur le dépôt du projet

---

# requirements.txt

```
# Dépendances de base pour Toolbox
# Aucune dépendance obligatoire pour le core

# Dépendances optionnelles pour les modules d'exemple
Pillow>=8.0.0          # Pour imgconv
requests>=2.25.0       # Pour les modules web
beautifulsoup4>=4.9.0  # Pour le parsing HTML
PyPDF2>=2.0.0         # Pour la manipulation PDF
python-magic>=0.4.0    # Détection de type MIME
```

---

# Exemples de modules supplémentaires

## Module de téléchargement de fichiers

```python
#!/usr/bin/env python3
"""
Module de téléchargement pour Toolbox
Télécharge des fichiers depuis des URLs
"""

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse

VERSION = "1.0.0"
DESCRIPTION = "Télécharge des fichiers depuis des URLs"

def download_file(url: str, output_path: str = None, show_progress: bool = True):
    """Télécharge un fichier depuis une URL"""
    try:
        import requests
        from tqdm import tqdm
    except ImportError:
        print("Erreur: Les modules 'requests' et 'tqdm' sont requis")
        print("Installez-les avec: pip install requests tqdm")
        return False
    
    try:
        # Détermine le nom de fichier si non spécifié
        if not output_path:
            parsed_url = urlparse(url)
            output_path = Path(parsed_url.path).name
            if not output_path:
                output_path = "downloaded_file"
        
        # Télécharge avec barre de progression
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f:
            if show_progress and total_size > 0:
                with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
            else:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        
        print(f"Fichier téléchargé: {output_path}")
        return True
        
    except Exception as e:
        print(f"Erreur lors du téléchargement: {e}")
        return False

def main(args):
    parser = argparse.ArgumentParser(description="Téléchargeur de fichiers")
    parser.add_argument('url', help='URL du fichier à télécharger')
    parser.add_argument('-o', '--output', help='Nom du fichier de sortie')
    parser.add_argument('--no-progress', action='store_true', 
                       help='Désactive la barre de progression')
    
    parsed_args = parser.parse_args(args)
    
    success = download_file(
        parsed_args.url, 
        parsed_args.output, 
        not parsed_args.no_progress
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

## Module de manipulation de texte

```python
#!/usr/bin/env python3
"""
Module de manipulation de texte pour Toolbox
Effectue diverses opérations sur les fichiers texte
"""

import argparse
import sys
from pathlib import Path
import re

VERSION = "1.0.0"
DESCRIPTION = "Manipule et transforme les fichiers texte"

def count_words(text: str) -> dict:
    """Compte les mots, lignes et caractères"""
    lines = text.split('\n')
    words = text.split()
    chars = len(text)
    chars_no_spaces = len(text.replace(' ', ''))
    
    return {
        'lines': len(lines),
        'words': len(words),
        'characters': chars,
        'characters_no_spaces': chars_no_spaces
    }

def find_replace(text: str, pattern: str, replacement: str, use_regex: bool = False) -> str:
    """Recherche et remplace du texte"""
    if use_regex:
        return re.sub(pattern, replacement, text)
    else:
        return text.replace(pattern, replacement)

def extract_emails(text: str) -> list:
    """Extrait les adresses email du texte"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)

def extract_urls(text: str) -> list:
    """Extrait les URLs du texte"""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)

def main(args):
    parser = argparse.ArgumentParser(
        description="Manipulation de fichiers texte",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  toolbox run text_tools --count fichier.txt
  toolbox run text_tools --replace "ancien" "nouveau" fichier.txt
  toolbox run text_tools --extract-emails fichier.txt
        """
    )
    
    parser.add_argument('file', help='Fichier texte à traiter')
    parser.add_argument('--count', action='store_true', help='Compte mots/lignes/caractères')
    parser.add_argument('--replace', nargs=2, metavar=('OLD', 'NEW'), 
                       help='Remplace OLD par NEW')
    parser.add_argument('--regex', action='store_true', 
                       help='Utilise les expressions régulières pour --replace')
    parser.add_argument('--extract-emails', action='store_true', 
                       help='Extrait les adresses email')
    parser.add_argument('--extract-urls', action='store_true', 
                       help='Extrait les URLs')
    parser.add_argument('-o', '--output', help='Fichier de sortie (pour --replace)')
    
    parsed_args = parser.parse_args(args)
    
    # Vérifie que le fichier existe
    if not Path(parsed_args.file).exists():
        print(f"Erreur: Le fichier '{parsed_args.file}' n'existe pas")
        return 1
    
    try:
        # Lit le fichier
        with open(parsed_args.file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Exécute l'opération demandée
        if parsed_args.count:
            stats = count_words(content)
            print(f"Statistiques pour '{parsed_args.file}':")
            print(f"  Lignes: {stats['lines']}")
            print(f"  Mots: {stats['words']}")
            print(f"  Caractères: {stats['characters']}")
            print(f"  Caractères (sans espaces): {stats['characters_no_spaces']}")
        
        elif parsed_args.replace:
            old_text, new_text = parsed_args.replace
            modified_content = find_replace(content, old_text, new_text, parsed_args.regex)
            
            output_file = parsed_args.output or parsed_args.file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            print(f"Remplacement effectué dans '{output_file}'")
        
        elif parsed_args.extract_emails:
            emails = extract_emails(content)
            if emails:
                print("Adresses email trouvées:")
                for email in sorted(set(emails)):
                    print(f"  {email}")
            else:
                print("Aucune adresse email trouvée")
        
        elif parsed_args.extract_urls:
            urls = extract_urls(content)
            if urls:
                print("URLs trouvées:")
                for url in sorted(set(urls)):
                    print(f"  {url}")
            else:
                print("Aucune URL trouvée")
        
        else:
            parser.print_help()
            return 1
        
        return 0
        
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

## Script de génération de modules

```python
#!/usr/bin/env python3
"""
Générateur de modules pour Toolbox
Crée la structure de base d'un nouveau module
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

def generate_module_template(name: str, description: str, author: str) -> str:
    """Génère le template d'un module"""
    template = f'''#!/usr/bin/env python3
"""
Module {name} pour Toolbox
{description}
"""

import argparse
import sys
from pathlib import Path

# Métadonnées du module
VERSION = "1.0.0"
DESCRIPTION = "{description}"
AUTHOR = "{author}"

def main(args):
    """Point d'entrée principal du module"""
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  toolbox run {name} --help
        """
    )
    
    # Ajoutez vos arguments ici
    parser.add_argument('--example', help='Argument d\\'exemple')
    
    # Parse les arguments
    parsed_args = parser.parse_args(args)
    
    # Votre logique ici
    print(f"Module {{DESCRIPTION}} v{{VERSION}}")
    print(f"Arguments reçus: {{args}}")
    
    # TODO: Implémentez votre fonctionnalité
    
    return 0

# Test direct du module
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''
    return template

def main():
    """Générateur de modules Toolbox"""
    print("=== Générateur de modules Toolbox ===")
    print()
    
    # Collecte les informations
    name = input("Nom du module: ").strip()
    if not name:
        print("Erreur: Le nom du module est requis")
        return 1
    
    description = input("Description: ").strip()
    if not description:
        description = f"Module {name}"
    
    author = input("Auteur: ").strip()
    if not author:
        author = "Toolbox User"
    
    # Génère le fichier
    filename = f"{name}.py"
    if Path(filename).exists():
        overwrite = input(f"Le fichier '{filename}' existe déjà. Écraser? (y/N): ")
        if overwrite.lower() != 'y':
            print("Génération annulée")
            return 0
    
    try:
        template = generate_module_template(name, description, author)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(template)
        
        # Rend exécutable sur Unix
        import os
        import stat
        if os.name != 'nt':  # Pas Windows
            st = os.stat(filename)
            os.chmod(filename, st.st_mode | stat.S_IEXEC)
        
        print(f"Module '{filename}' généré avec succès!")
        print()
        print("Prochaines étapes:")
        print(f"  1. Éditez '{filename}' pour implémenter votre logique")
        print(f"  2. Testez avec: python {filename} --help")
        print(f"  3. Installez avec: toolbox install {filename}")
        
        return 0
        
    except Exception as e:
        print(f"Erreur lors de la génération: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```