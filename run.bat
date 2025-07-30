@echo off
echo Lancement du Traducteur de Texte Chinois...
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ERREUR: Impossible de lancer l'application
    echo Vérifiez que toutes les dépendances sont installées
    echo.
    pause
) 