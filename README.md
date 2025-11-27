![Toolbox](Logo/white_Logo.png)

# Toolbox - Gestionnaire de modules Python

## Description

Toolbox est une application en ligne de commande modulaire qui permet d'exécuter des scripts Python comme des modules interchangeables. L'idée est de pouvoir réaliser en local toutes les opérations que proposent les sites web (conversion d'images, manipulation de fichiers, etc.).

## Pourquoi ToolBox ?

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

Ce projet est sous licence (LOC)[loc.zyglonk.fr]

## Support

Pour obtenir de l'aide :

- Consultez cette documentation
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
