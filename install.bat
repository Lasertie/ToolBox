@echo off
REM install.bat - Script d'installation pour Windows
setlocal enabledelayedexpansion

echo === Installation de Modular CLI ===
echo.

REM Variables
set "PYTHON_CMD="
set "PIP_CMD="
set "USE_VENV="

REM Fonction pour afficher les messages colorés (limité sur Windows)
:print_status
echo [INFO] %~1
goto :eof

:print_success
echo [SUCCESS] %~1
goto :eof

:print_warning
echo [WARNING] %~1
goto :eof

:print_error
echo [ERROR] %~1
goto :eof

REM Vérifier Python
:check_python
call :print_status "Vérification de Python..."

where python >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
) else (
    where python3 >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python3"
    ) else (
        call :print_error "Python n'est pas installé ou n'est pas dans le PATH"
        echo Téléchargez Python depuis https://python.org
        pause
        exit /b 1
    )
)

REM Vérifier la version de Python
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set "PYTHON_VERSION=%%i"
call :print_success "Python %PYTHON_VERSION% détecté"
goto :eof

REM Vérifier pip
:check_pip
call :print_status "Vérification de pip..."

where pip >nul 2>&1
if %errorlevel% equ 0 (
    set "PIP_CMD=pip"
) else (
    %PYTHON_CMD% -m pip --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PIP_CMD=%PYTHON_CMD% -m pip"
    ) else (
        call :print_error "pip n'est pas installé"
        call :print_status "Installation de pip..."
        %PYTHON_CMD% -m ensurepip --upgrade
        set "PIP_CMD=%PYTHON_CMD% -m pip"
    )
)

call :print_success "pip disponible"
goto :eof

REM Créer l'environnement virtuel
:setup_venv
if "%USE_VENV%"=="1" (
    call :print_status "Création d'un environnement virtuel..."
    
    if not exist "venv" (
        %PYTHON_CMD% -m venv venv
    )
    
    REM Activer l'environnement virtuel
    call venv\Scripts\activate.bat
    set "PIP_CMD=pip"
    
    call :print_success "Environnement virtuel activé"
)
goto :eof

REM Installation des dépendances
:install_dependencies
call :print_status "Installation des dépendances..."

REM Mise à jour de pip
%PIP_CMD% install --upgrade pip

REM Installation des dépendances principales
%PIP_CMD% install Pillow

call :print_success "Dépendances installées"
goto :eof

REM Installation de l'application
:install_app
call :print_status "Installation de Modular CLI..."

if exist "setup.py" (
    %PIP_CMD% install -e .
) else (
    %PIP_CMD% install toolbox
)

call :print_success "Modular CLI installé"
goto :eof

REM Créer le répertoire des modules
:setup_modules_dir
call :print_status "Configuration du répertoire des modules..."

set "MODULES_DIR=%USERPROFILE%\.toolbox\modules"
if not exist "%MODULES_DIR%" mkdir "%MODULES_DIR%"

REM Copier les modules exemples s'ils existent
if exist "modules" (
    copy /Y "modules\*.py" "%MODULES_DIR%\" >nul 2>&1
)

call :print_success "Répertoire des modules configuré: %MODULES_DIR%"
goto :eof

REM Test de l'installation
:test_installation
call :print_status "Test de l'installation..."

where toolbox >nul 2>&1
if %errorlevel% equ 0 (
    call :print_success "toolbox installé avec succès!"
    toolbox list
) else (
    call :print_warning "toolbox n'est pas dans le PATH"
    call :print_status "Vous pouvez l'exécuter avec: %PYTHON_CMD% -m toolbox"
)
goto :eof

REM Affichage de l'aide
:show_help
echo Usage: %~nx0 [OPTIONS]
echo.
echo Options:
echo   --venv          Installer dans un environnement virtuel
echo   --help          Afficher cette aide
echo.
goto :eof

REM Parse des arguments
:parse_args
if "%~1"=="--venv" (
    set "USE_VENV=1"
    shift
    goto parse_args
)
if "%~1"=="--help" (
    call :show_help
    exit /b 0
)
if not "%~1"=="" (
    call :print_error "Option inconnue: %~1"
    call :show_help
    exit /b 1
)
goto :eof

REM Fonction principale
:main
call :print_status "Début de l'installation..."

call :check_python
call :check_pip
call :setup_venv
call :install_dependencies
call :install_app
call :setup_modules_dir
call :test_installation

echo.
call :print_success "Installation terminée!"
echo.
echo Utilisation:
echo   toolbox list                                    # Lister les modules
echo   toolbox run image-converter --help              # Aide pour un module
echo   toolbox run image-converter --input image.jpg --format png
echo.

pause
goto :eof

REM Exécution principale
call :parse_args %*
call :main