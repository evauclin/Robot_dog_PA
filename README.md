## Description

L'objectif de ce projet est de créer un robot chien capable de reconnaître son maître, d'avancer vers lui jusqu'à ses pieds. Le robot est contrôlé par un Raspberry Pi.

## Configuration

### Raspberry Pi
La première étape de configuration consiste à cloner le référentiel git du robot chien Freenove sur le Raspberry Pi. Suivez la documentation du robot chien Freenove pour configurer correctement le Raspberry Pi avec le système du robot. 

### API
La deuxième étape de configuration concerne l'API, qui est codée en FastAPI et sera déployée sur une machine virtuelle AWS à l'aide de Docker. La construction de l'API se fera directement via un fichier Dockerfile situé à la racine du projet.

## Technologies utilisées

* FastAPI : framework web moderne et rapide pour construire l'API.


* Docker : plateforme permettant de développer, de livrer et d'exécuter des applications dans des conteneurs.


* Raspberry Pi : nano-ordinateur monocarte utilisé pour contrôler le robot.


* Python : langage de programmation utilisé pour coder l'API et le système de contrôle du robot.


* DistanceMeasurement (YOLO) : bibliothèque de détection d'objets couplée avec une stratégie algorithmique pour estimer une distance entre le robot et l'humain détecté.


* FaceRecognition (ResNetModel) : bibliothèque de reconnaissance faciale utilisée pour reconnaître le maître du robot.


## Installation
Clonez le référentiel git du robot chien Freenove sur le Raspberry Pi.
Suivez la documentation du robot chien Freenove pour configurer correctement le Raspberry Pi avec le système du robot.
Construisez l'image Docker de l'API en utilisant le fichier Dockerfile situé à la racine du projet.
Déployez l'image Docker de l'API sur une machine virtuelle AWS.
Utilisation
Une fois l'API déployée et le Raspberry Pi configuré, le robot chien devrait être capable de reconnaître son maître et d'avancer vers lui jusqu'à ses pieds tout en détectant la distance entre eux.

## Ressources 

* Documentation robot chien Freenove : https://freenove.com/fnk0050/

* Lien amazon robot : https://www.amazon.com/gp/product/B08C254F73/ref=as_li_qf_asin_il_tl?ie=UTF8&tag=fuzzysloth-20&creative=9325&linkCode=as2&creativeASIN=B08C254F73&linkId=0b757302657cc14957f6ae4c0a0ec6d0



