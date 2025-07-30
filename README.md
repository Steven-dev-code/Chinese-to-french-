# Traducteur de Texte Chinois

Une application Python pour capturer du texte chinois avec une caméra et le traduire en français.

## Fonctionnalités

- 📷 **Capture d'image** : Utilisez votre webcam pour capturer du texte chinois
- 📁 **Chargement d'image** : Importez des images existantes depuis votre ordinateur
- 🔍 **Reconnaissance de texte** : Détection automatique du texte chinois avec EasyOCR
- 🔄 **Traduction automatique** : Traduction en français avec Google Translate
- 💾 **Sauvegarde** : Enregistrez vos résultats dans un fichier texte
- 🎨 **Interface intuitive** : Interface graphique moderne et facile à utiliser

## Prérequis

- Python 3.7 ou supérieur
- Webcam (pour la capture d'image)
- Connexion Internet (pour la traduction)

## Installation

1. **Cloner ou télécharger le projet**
   ```bash
   git clone <url-du-repo>
   cd video
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python main.py
   ```

## Utilisation

### Capture avec la caméra
1. Cliquez sur "📷 Capturer" pour activer votre webcam
2. Positionnez le texte chinois devant la caméra
3. Cliquez sur "📸 Capturer l'Image" pour prendre la photo
4. Cliquez sur "🔄 Traduire" pour lancer la reconnaissance et la traduction

### Chargement d'image
1. Cliquez sur "📁 Charger Image"
2. Sélectionnez une image contenant du texte chinois
3. Cliquez sur "🔄 Traduire" pour lancer la reconnaissance et la traduction

### Sauvegarde des résultats
1. Après la traduction, cliquez sur "💾 Sauvegarder"
2. Choisissez l'emplacement et le nom du fichier
3. Les résultats seront sauvegardés au format texte

## Technologies utilisées

- **OpenCV** : Capture d'image et traitement
- **EasyOCR** : Reconnaissance optique de caractères (OCR)
- **Google Translate** : Traduction automatique
- **Tkinter** : Interface graphique
- **Pillow** : Manipulation d'images

## Structure du projet

```
video/
├── main.py              # Application principale
├── requirements.txt     # Dépendances Python
└── README.md           # Documentation
```

## Dépannage

### Problèmes courants

1. **Erreur de caméra**
   - Vérifiez que votre webcam est connectée et fonctionne
   - Assurez-vous qu'aucune autre application n'utilise la caméra

2. **Erreur de reconnaissance**
   - Assurez-vous que le texte est bien visible et lisible
   - Améliorez l'éclairage si nécessaire
   - Vérifiez que le texte est en chinois simplifié ou traditionnel

3. **Erreur de traduction**
   - Vérifiez votre connexion Internet
   - Assurez-vous que le texte a été correctement détecté

### Installation des modèles EasyOCR

Lors de la première utilisation, EasyOCR téléchargera automatiquement les modèles de reconnaissance pour le chinois. Cela peut prendre quelques minutes selon votre connexion Internet.

## Licence

Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le distribuer.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouvelles fonctionnalités

## Support

Si vous rencontrez des problèmes, veuillez :
1. Vérifier que toutes les dépendances sont installées
2. Consulter la section dépannage
3. Créer une issue sur le repository avec les détails du problème 