@echo off
echo Lancement du Traducteur de Texte Chinois (Version Alternative)...
echo.

python main_alternative.py

if errorlevel 1 (
    echo.
    echo ERREUR: Impossible de lancer l'application
    echo Vérifiez que toutes les dépendances sont installées
    echo.
    pause
) 