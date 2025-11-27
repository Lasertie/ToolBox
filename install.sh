#!/bin/bash
# install.sh - Script d'installation pour Linux/macOS

set -e

echo "=== Installation de Toolbox ==="

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage coloré
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Vérifier Python
check_python() {
    print_status "Vérification de Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python n'est pas installé ou n'est pas dans le PATH"
        exit 1
    fi
    
    # Vérifier la version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    MAJOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR_VERSION=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$MAJOR_VERSION" -lt 3 ] || ([ "$MAJOR_VERSION" -eq 3 ] && [ "$MINOR_VERSION" -lt 7 ]); then
        print_error "Python 3.7+ requis (version détectée: $PYTHON_VERSION)"
        exit 1
    fi
    
    print_success "Python $PYTHON_VERSION détecté"
}

# Vérifier pip
check_pip() {
    print_status "Vérification de pip..."
    
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        print_error "pip n'est pas installé"
        print_status "Installation de pip..."
        $PYTHON_CMD -m ensurepip --upgrade
        PIP_CMD="$PYTHON_CMD -m pip"
    fi
    
    print_success "pip disponible"
}

# Créer l'environnement virtuel (optionnel)
setup_venv() {
    if [ "$1" = "--venv" ]; then
        print_status "Création d'un environnement virtuel..."
        
        if [ ! -d "venv" ]; then
            $PYTHON_CMD -m venv venv
        fi
        
        # Activer l'environnement virtuel
        source ./venv/bin/activate
        PIP_CMD="pip"
        
        print_success "Environnement virtuel activé"
    fi
}

# Installation des dépendances
install_dependencies() {
    print_status "Installation des dépendances..."
    
    # Mise à jour de pip
    $PIP_CMD install --upgrade pip
    
    # Installation des dépendances principales
    $PIP_CMD install Pillow
    
    print_success "Dépendances installées"
}

# Installation de l'application
install_app() {
    print_status "Installation de Toolbox..."
    
    # Si nous sommes dans le répertoire source
    if [ -f "setup.py" ]; then
        $PIP_CMD install -e .
    else
        # Installation depuis PyPI (quand disponible)
        $PIP_CMD install toolbox
    fi
    
    print_success "Toolbox installé"
}

# Créer le répertoire des modules
setup_modules_dir() {
    print_status "Configuration du répertoire des modules..."
    
    MODULES_DIR="$HOME/.toolbox/modules"
    mkdir -p "$MODULES_DIR"
    
    # Copier les modules exemples s'ils existent
    if [ -d "modules" ]; then
        cp modules/*.py "$MODULES_DIR/" 2>/dev/null || true
    fi
    
    print_success "Répertoire des modules configuré: $MODULES_DIR"
}

# Test de l'installation
test_installation() {
    print_status "Test de l'installation..."
    
    if command -v toolbox &> /dev/null; then
        print_success "toolbox installé avec succès!"
        toolbox list
    else
        print_warning "toolbox n'est pas dans le PATH"
        print_status "Vous pouvez l'exécuter avec: $PYTHON_CMD -m toolbox"
    fi
}

# Affichage de l'aide
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --venv          Installer dans un environnement virtuel"
    echo "  --help          Afficher cette aide"
    echo ""
}

# Parse des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --venv)
            USE_VENV="--venv"
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            print_error "Option inconnue: $1"
            show_help
            exit 1
            ;;
    esac
done

# Exécution principale
main() {
    print_status "Début de l'installation..."
    
    check_python
    check_pip
    setup_venv $USE_VENV
    install_dependencies
    install_app
    setup_modules_dir
    test_installation
    
    echo ""
    print_success "Installation terminée!"
    echo ""
    echo "Utilisation:"
    echo "  toolbox list                    # Lister les modules"
    echo "  toolbox imgconv --help  # Aide pour un module"
    echo "  toolbox imgconv --input image.jpg --format png"
    echo ""
}

# Vérifier si le script est exécuté directement
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi