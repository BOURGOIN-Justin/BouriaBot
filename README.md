# 🛠️ NG Build Bot - NationsGlory

Un bot Discord utilitaire pour les builders sur NationsGlory
## Fonctionnalités
* **Analyse de Schematics :** Lit automatiquement les fichiers `.schematic` postés sur Discord pour extraire et compter chaque bloc.
* **Calcul instantané des coûts :** Croise les données extraites avec une base de prix locale pour générer un devis précis. Les blocs gratuits (minerais, terre, etc.) sont intelligemment ignorés (0$).
* **Génération de factures Excel :** Crée un fichier Excel (`.xlsx`) téléchargeable via un bouton interactif sur Discord avec le détail exact des blocs à farm.
* **Interface moderne :** Utilise les commandes Slash Discord (`/devis`, `/ping`) pour une expérience utilisateur fluide.
* **Répertoire des commandes World Edit:** Permet de retrouver les commandes utiles lors du build afin de ne pas avoir à "recréer" les commandes à chaque fois.
* **Envoi moderne :** Permet d'envoyer un message avec les coordonnées et le fichier .schematic à construire en jeu dans un salon spécifique (rôle spécifique requis pour utiliser la commande sur le serveur cible).
* 
## ⚙️ Prérequis
* **Python 3.8+**
* Un serveur d'hébergement 24/7 (ex: Raspberry Pi sous Linux).
* Les bases de données JSON incluses dans ce dépôt (`all.json` et `prix.json`).

## Installation & Déploiement (Linux / Raspberry Pi)

**1. Récupérer le projet :**
```bash
git clone https://github.com/BOURGOIN-Justin/Bot-discord-NationsGlory.git
cd Bot-discord-NationsGlory
```

**2. Installer les dépendances :**
```bash
pip install discord nbt openpyxl
```

**3. Configurer la sécurité :**
Créez un fichier texte nommé `token.txt` à la racine du projet et collez-y **uniquement** le Token de votre bot Discord. Ce fichier est ignoré par Git pour des raisons de sécurité.

**4. Lancer le bot en arrière-plan :**
Pour que le bot tourne 24h/24 même quand vous fermez votre terminal, utilisez `screen` :
```bash
screen -S ngbot
python3 ng_build_bot.py
```
*(Appuyez sur `Ctrl+A` puis `D` pour détacher l'écran et laisser le bot travailler !)*

## Configuration de l'économie
Pour modifier le prix des blocs ou ajuster l'économie en fonction de vos besoins, il suffit de modifier les valeurs dans le fichier `prix.json`. Le bot prendra en compte les nouveaux tarifs dynamiquement à la prochaine commande `/devis` !

---
*Projet développé pour l'automatisation de la gestion des builds sur NationsGlory.*