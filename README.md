**Fonctionnalités** 

    --> Analyse de Schematics : Lit automatiquement les fichiers .schematic postés sur Discord pour extraire et compter chaque bloc.

    --> Calcul instantané des coûts : Croise les données extraites avec une base de prix locale pour générer un devis précis. Les blocs gratuits (minerais, terre, etc.) sont ignorés (0$).

    --> Génération de factures Excel : Crée un fichier Excel (.xlsx) téléchargeable via un bouton interactif sur Discord avec le détail exact des blocs à récupérer.

    --> Interface moderne : Utilise les commandes Slash Discord (/devis, /ping) pour une expérience utilisateur fluide.

**⚙️ Prérequis pour la mise en place du bot**

    --> Python 3.8+

    --> Un serveur d'hébergement 24/7 (ex: Raspberry Pi sous Linux).

    --> Les bases de données JSON incluses dans ce dépôt (all.json et prix.json).

**🚀 Installation & Déploiement (Linux / Raspberry Pi)**
1. Récupérer le projet :

Bash
git clone https://github.com/BOURGOIN-Justin/Bot-discord-NationsGlory.git
cd Bot-discord-NationsGlory
2. Installer les dépendances :

Bash
pip install discord nbt openpyxl
3. Configurer la sécurité :
Créez un fichier texte nommé token.txt à la racine du projet et collez-y uniquement le Token de votre bot Discord. Ce fichier est ignoré par Git pour des raisons de sécurité.

4. Lancer le bot en arrière-plan :
Pour que le bot tourne 24h/24 même quand vous fermez votre terminal, utilisez screen :

Bash
screen -S ngbot
python3 ng_build_bot.py
(Appuyez sur Ctrl+A puis D pour détacher l'écran et laisser le bot travailler !)

🧮 Configuration de l'économie
Pour modifier le prix des blocs ou ajuster l'économie en fonction de votre pays sur NationsGlory, il suffit de modifier les valeurs dans le fichier prix.json. Le bot prendra en compte les nouveaux tarifs dynamiquement à la prochaine commande /devis !

Projet développé pour l'automatisation et la gestion des builds sur NationsGlory.