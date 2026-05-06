from nbt import nbt
from collections import Counter
import json
import os

FICHIER_MEMOIRE = "prix.json"


def sauvegarder_prix(nom_bloc, prix_bloc):

    if os.path.exists("prix.json"):
        with open("prix.json", 'r', encoding='utf-8') as f:
            memoire = json.load(f)
    else:
        memoire = {}

    memoire[nom_bloc] = prix_bloc

    with open("prix.json", 'w', encoding='utf-8') as f:
        json.dump(memoire, f, indent=4, ensure_ascii=False)

    print(f"{nom_bloc}) a été sauvegardé définitivement !")

def lecture_schematic(name, dicoB, dicoP):
    nbtfile = nbt.NBTFile(name, 'rb')
    print("Clés du fichier :", nbtfile.keys())

    blocks = nbtfile['Blocks'].value
    data = nbtfile['Data'].value
    add_blocks = nbtfile['AddBlocks'].value if 'AddBlocks' in nbtfile else None

    liste_ids_complets = []

    for i in range(len(blocks)):
        vrai_id = blocks[i]

        if add_blocks:
            add_val = (add_blocks[i // 2] >> (0 if i % 2 else 4)) & 0x0F
            vrai_id = (add_val << 8) + vrai_id

        if vrai_id != 0:
            cle_format = f"{vrai_id}:{data[i]}"
            liste_ids_complets.append(cle_format)

    count = Counter(liste_ids_complets)

    prix_total = 0

    for cle_recherche, quantite in count.items():

        nom_du_bloc = dicoB.get(cle_recherche, "Bloc Inconnu")
        if nom_du_bloc == "Bloc Inconnu":
            print(f"ID inexistant : {cle_recherche}")
            nom = input("Veuillez saisir Le nom du bloc : ")

            dicoB[cle_recherche] = nom
            nom_du_bloc = nom
    
            with open('all.json', 'w', encoding='utf-8') as fichier:

                json.dump(dicoB, fichier, indent=4, ensure_ascii=False)
        #prix_bloc = dicoP.get(nom_du_bloc, "Prix inconnu")

        #if prix_bloc == "Prix inconnu":
            #print(f"Prix inexistant : {dicoB[cle_recherche]}")
            #prix = float(input("Veuillez saisir Le prix bloc : "))
            #dicoP[nom_du_bloc] = prix
           # prix_bloc = prix
            #sauvegarder_prix(nom_du_bloc, prix)
        #sous_total = prix_bloc * quantite
        #prix_total += sous_total
        print(f"ID Minecraft [{cle_recherche}] : {quantite} blocs | name : {nom_du_bloc}")

    print("-" * 40)
    print("Nombre de blocs au total:", sum(count.values()))
    print("Prix du schematic: ", prix_total)


def lecture_fichier_json(name):
    with open(name, 'r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)

    donnees_lisibles = {}
    for bloc in donnees:

        data_val = bloc.get("Data", 0)

        cle = f"{bloc['block_id']}:{data_val}"

        donnees_lisibles[cle] = bloc["display_name_fr"]

    print("Données chargées: ", len(donnees_lisibles))
    return donnees_lisibles


# --- LANCEMENT DU SCRIPT ---

with open("all.json", 'r', encoding='utf-8') as fichier:
    donnees_totale = json.load(fichier)
with open("prix.json", 'r', encoding='utf-8') as f_prix:
    donnees_prix = json.load(f_prix)

# Appel de la fonction
lecture_schematic("PapoushopRDC.schematic", donnees_totale, donnees_prix)