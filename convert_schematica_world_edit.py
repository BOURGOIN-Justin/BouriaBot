import sys
import os

try:
    from nbt import nbt
except ImportError:
    print("Erreur : La librairie 'nbt' n'est pas installee.")
    print("Ouvrez la commande (cmd) et tapez : pip install nbt")
    sys.exit(1)


def convert_schematica_to_worldedit(input_filename, output_filename):
    print(f"Chargement du fichier {input_filename}... Cela peut prendre quelques secondes pour un gros fichier.")

    if not os.path.exists(input_filename):
        print(f"Erreur : Le fichier {input_filename} est introuvable dans ce dossier.")
        return

    try:
        # Ouverture du fichier NBT compressé
        schem = nbt.NBTFile(input_filename, 'rb')

        # Vérification de la présence des blocs moddés (AddBlocks)
        if 'AddBlocks' in schem:
            add_blocks = schem['AddBlocks'].value
            new_add_blocks = bytearray(len(add_blocks))

            print(f"Correction de {len(add_blocks)} octets d'ID moddés en cours...")

            # Inversion des paires de bits (Nibble Swap)
            for i in range(len(add_blocks)):
                b = add_blocks[i]
                # On inverse les 4 bits de gauche avec les 4 bits de droite
                new_b = ((b & 0x0F) << 4) | ((b & 0xF0) >> 4)
                new_add_blocks[i] = new_b

            # Remplacement de l'ancienne valeur par la nouvelle
            schem['AddBlocks'].value = new_add_blocks

            # Sauvegarde du nouveau fichier
            schem.write_file(output_filename)
            print(f"Succes ! Fichier converti et sauvegarde sous : {output_filename}")

        else:
            print("Le fichier ne contient pas de blocs moddes avec un ID superieur a 255.")
            print("Il devrait deja etre 100% compatible avec WorldEdit.")

    except Exception as e:
        print(f"Une erreur technique s'est produite : {e}")


# Lancement du script
fichier_original = "lastmaroc.schematic"
fichier_converti = "lastmaroc_we.schematic"

convert_schematica_to_worldedit(fichier_original, fichier_converti)