# README

## EasyExport Algorithm

### Description
Le script `EasyExportAlgorithm` a été développé par Mohamed RIZKI, étudiant en 2ème année cycle ingénieur. Ce script permet d'exporter des plans en PDF en utilisant les layouts définis dans un projet QGIS. Il permet de sélectionner un layout, une couche à exclure, de définir les recouvrements horizontaux et verticaux, et de spécifier le chemin d'exportation.

### Prérequis

1. **QGIS** : Assurez-vous d'avoir QGIS installé (version 3.10 ou supérieure).
2. **Script Python** : Vous aurez besoin du script Python `EasyExportAlgorithm.py`.

### Installation

1. **Télécharger le script** : Téléchargez le script `EasyExportAlgorithm.py` et placez-le dans un répertoire de votre choix.
2. **Ouvrir QGIS** : Lancez QGIS.
3. **Charger le script** : Ouvrez votre script dans QGIS et exécutez-le.

### Utilisation

Une fois le script chargé, exécutez-le. Voici les étapes pour utiliser le script :

### Paramètres de l'algorithme

1. **Sélectionner un Layout** :
   - **Description** : Choisissez un layout parmi ceux définis dans votre projet QGIS.
   - **Type** : Liste déroulante.
   - **Optionnel** : Non.

2. **Couche à ne pas prendre en compte (Optionnel)** :
   - **Description** : Sélectionnez une couche à exclure du calcul de l'étendue visible. Cela est particulièrement utile pour exclure des fonds de carte comme OpenStreetMap, car leur inclusion peut entraîner la génération de plans vides et blancs.
   - **Type** : Sélection de couche.
   - **Optionnel** : Oui.

3. **Recouvrement Horizontal (%)** :
   - **Description** : Définissez le pourcentage de recouvrement horizontal entre les plans exportées.
   - **Type** : Numérique (pourcentage).
   - **Optionnel** : Oui.
   - **Valeur par défaut** : 0.

4. **Recouvrement Vertical (%)** :
   - **Description** : Définissez le pourcentage de Recouvrement vertical entre les plans exportées.
   - **Type** : Numérique (pourcentage).
   - **Optionnel** : Oui.
   - **Valeur par défaut** : 0.

5. **Chemin d'exportation** :
   - **Description** : Spécifiez le chemin d'exportation pour les fichiers PDF générés. Chaque fichier sera nommé avec un suffixe indiquant son numéro de page.
   - **Type** : Destination de fichier (PDF).
   - **Optionnel** : Non.

### Exemple de sortie

Lorsque vous exécutez l'algorithme, il :

1. Calcule les dimensions du layout sélectionné.
2. Calcule l'étendue visible des couches dans le projet QGIS, en excluant la couche spécifiée.
3. Divise cette étendue en plusieurs rectangles en fonction des dimensions du layout et des recouvrements spécifiés.
4. Exporte chaque rectangle en tant que fichier PDF distinct, en utilisant le layout sélectionné.

### Remarques

- Assurez-vous que les couches à inclure dans l'étendue visible sont activées (visibles) dans le projet QGIS.
- Le recouvrement permet d'assurer une continuité visuelle entre les plans exportées.
- Les fichiers PDF exportés seront nommés avec un suffixe numérique pour indiquer leur ordre (par exemple, `export_path_1.pdf`, `export_path_2.pdf`, etc.).

### Contact

Pour toute question ou suggestion, vous pouvez me contacter par mail : Mohamedrizki07@gmail.com
