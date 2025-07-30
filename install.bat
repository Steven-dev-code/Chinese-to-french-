@echo off
echo ========================================
echo Installation du Traducteur de Texte Chinois
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

echo Installation des dépendances...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERREUR: Échec de l'installation des dépendances
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation terminée avec succès!
echo ========================================
echo.
echo Pour lancer l'application, exécutez:
echo python main.py
echo.
pause 