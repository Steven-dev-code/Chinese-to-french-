@echo off
echo ========================================
echo Installation du Traducteur de Texte Chinois (Version Alternative)
echo ========================================
echo.

echo Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

echo Python détecté avec succès!
echo.

echo Installation des dépendances (version alternative)...
pip install -r requirements_alternative.txt

if errorlevel 1 (
    echo ERREUR: Échec de l'installation des dépendances
    echo Tentative avec des versions plus récentes...
    pip install opencv-python easyocr Pillow numpy requests
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer les dépendances
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Installation terminée avec succès!
echo ========================================
echo.
echo Pour lancer l'application, exécutez:
echo python main_alternative.py
echo.
pause 