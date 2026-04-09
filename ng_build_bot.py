import discord
from discord.ext import commands
from discord import app_commands
from nbt import nbt
from collections import Counter
import json
import os
import openpyxl

def generer_excel_farm(nom_schematic, inventaire_blocs, dico_noms, dico_prix):
    """
    Permet de générer un document excel répertoriant le nom des blocs, la quantité et le prix associé
    Args:
        nom_schematic (str) : Le nom du fichier en schematic.
        inventaire_blocs (dict) : Dictionnaire qui contient les IDs et une quantité associée.
        dico_noms (dict) : Dictionnaire qui contient les IDs et un nom associé.
        dico_prix(dict) : Dictionnaire qui contient le nom des blocs et un prix associé.
    Returns:
        str : Nom du fichier excel généré.

    """
    # On crée le fichier Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Liste de Farm"

    # En-têtes des colonnes
    ws.append(["Nom du Bloc", "ID", "Quantité", "Prix Total ($)"])

    # On remplit ligne par ligne
    for id_bloc, quantite in inventaire_blocs.items():
        # On cherche le nom via l'ID
        nom = dico_noms.get(id_bloc, "Inconnu")
        # On cherche le prix via le nom
        prix_unitaire = dico_prix.get(nom, 0)
        total_prix = quantite * prix_unitaire

        ws.append([nom, id_bloc, quantite, total_prix])

    # On sauvegarde avec un nom propre
    nom_fichier = f"Liste_Farm_{nom_schematic}.xlsx"
    wb.save(nom_fichier)
    return nom_fichier

def lecture_schematic(name, dicoB, dicoP):
    """
    Permet de lire un fichier au format schematic
    Args:
        name (str) : Nom du fichier à analyser
        dicoB (dict) : Dictionnaire qui contient les IDs de blocs et le nom associé
        dicoP (dict) : Dictionnaire qui contient le nom de blocs et leur prix associé

    Returns:
        float : Prix total du schematic
        list : Liste des blocs manquants
        int : Nombre total de blocs du schematic
        dict : Dictionnaire qui contient les IDs de blocs et une quantité associé
    """
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
    blocs_manquants = []

    for cle_recherche, quantite in count.items():
        nom_du_bloc = dicoB.get(cle_recherche, "Bloc Inconnu")
        if nom_du_bloc == "Bloc Inconnu":
            print(f"ID inexistant : {cle_recherche}")
            if cle_recherche not in blocs_manquants:
                blocs_manquants.append(cle_recherche)
            with open('all.json', 'w', encoding='utf-8') as fichier:
                json.dump(dicoB, fichier, indent=4, ensure_ascii=False)
        prix_bloc = dicoP.get(nom_du_bloc, 0)
        sous_total = prix_bloc * quantite
        prix_total += sous_total
        print(f"ID Minecraft [{cle_recherche}] : {quantite} blocs | name : {nom_du_bloc}")
    print("-" * 40)
    print("Nombre de blocs au total:", sum(count.values()))
    print("Prix du schematic: ", prix_total)
    return prix_total, blocs_manquants, sum(count.values()), count

def lecture_fichier_json(name):
    """
    Permet de lire un fichier au format json
    Args:
        name (str) : Nom du fichier au format json à lire
    """
    with open(name, 'r', encoding='utf-8') as fichier:
        donnees = json.load(fichier)
    donnees_lisibles = {}
    for bloc in donnees:
        data_val = bloc.get("Data", 0)
        cle = f"{bloc['block_id']}:{data_val}"
        donnees_lisibles[cle] = bloc["display_name_fr"]
    print("Données chargées: ", len(donnees_lisibles))
    return donnees_lisibles

class NGBuildBot(commands.Bot):
    def __init__(self):
        # Configuration des intents
        intents = discord.Intents.default()
        intents.message_content = True
        # On initialise avec un préfixe bidon car on utilise les Slash Commands
        super().__init__(command_prefix="!", intents=intents)
    # Cette fonction synchronise les commandes "/" avec Discord au démarrage
    async def setup_hook(self):
        await self.tree.sync()
        print("🔄 Commandes Slash synchronisées avec succès !")
bot = NGBuildBot()

@bot.event
async def on_ready():
    print(f'✅ Connecté en tant que {bot.user} !')
    print('Le bot est prêt à recevoir des commandes.')

@bot.tree.command(name="ping", description="Vérifie si le bot est en ligne")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong ! Je suis bien en ligne et prêt à analyser tes schematics !")


class BoutonExcel(discord.ui.View):
    def __init__(self, nom_propre, count, donnees_totale, donnees_prix):
        super().__init__(timeout=None)  # Le bouton ne se désactive jamais
        # On sauvegarde les données en mémoire pour quand le joueur cliquera
        self.nom_propre = nom_propre
        self.count = count
        self.donnees_totale = donnees_totale
        self.donnees_prix = donnees_prix

    @discord.ui.button(label="📊 Télécharger l'Excel", style=discord.ButtonStyle.green)
    async def telecharger(self, interaction: discord.Interaction, button: discord.ui.Button):
        # On indique qu'on prépare le fichier (en mode invisible pour les autres)
        await interaction.response.defer(ephemeral=True)

        # On génère le fichier UNIQUEMENT au moment du clic
        nom_temp = f"temp_{interaction.id}"
        generation_excel = generer_excel_farm(nom_temp, self.count, self.donnees_totale, self.donnees_prix)
        with open(generation_excel, 'rb') as f:
            discord_file = discord.File(f, filename=f"Farm_{self.nom_propre}.xlsx")
            await interaction.followup.send(content="Voici ton fichier :", file=discord_file)

        # On supprime le fichier après l'envoi
        if os.path.exists(generation_excel):
            os.remove(generation_excel)


@bot.tree.command(name="devis", description="Génère un devis à partir d'un fichier .schematic")
@app_commands.describe(fichier="Le fichier .schematic à analyser")
async def devis(interaction: discord.Interaction, fichier: discord.Attachment):
    # Vérification de l'extension du fichier
    if not fichier.filename.endswith(".schematic"):
        # L'argument ephemeral=True rend le message visible uniquement par celui qui a tapé la commande
        await interaction.response.send_message("❌ Erreur : Le fichier doit être un `.schematic` !", ephemeral=True)
        return
    # On indique à Discord que le bot "réfléchit" pour éviter qu'il affiche "L'application n'a pas répondu"
    await interaction.response.defer()
    try:
        # Chargement des bases de données JSON
        with open("all.json", 'r', encoding='utf-8') as fichiertot:
            donnees_totale = json.load(fichiertot)
        with open("prix.json", 'r', encoding='utf-8') as f_prix:
            donnees_prix = json.load(f_prix)
        # Sauvegarde temporaire du fichier sur le Raspberry Pi
        chemin_local = fichier.filename
        await fichier.save(chemin_local)

        # Lancement de ton algorithme de calcul
        prix, liste_erreurs, blocks_total, count = lecture_schematic(chemin_local, donnees_totale, donnees_prix)
        nom_propre = fichier.filename.replace('.schematic', '')
        couleur_facture = discord.Color.red() if len(liste_erreurs) > 0 else discord.Color.green()

        # Création de la facture
        facture = discord.Embed(
            title=f"<:Groupfqsf:1431359830676996167>  Devis pour le schematic : **{nom_propre}**",
            description="Voici l'analyse des coûts. Les blocs obtenables gratuitement sont comptabilisés à 0$ (Marbre, minerais, etc).",
            color=couleur_facture
        )
        facture.set_thumbnail(url=bot.user.display_avatar.url)
        facture.add_field(name="<:28993mcgrassblock:1406936610746007622> Nombre de blocs", value=f"**{blocks_total}**", inline=True)
        facture.add_field(name="<:itemmoney:1403438157596196906> Prix total", value=f"**{prix} $**", inline=False)
        facture.add_field(name="", value="", inline=False)

        # Gestion des blocs inconnus
        if len(liste_erreurs) > 0:
            premiers_ids = liste_erreurs[:10]
            texte_erreur = "\n 🔸ID " + "\n 🔸ID ".join(premiers_ids)
            message_erreur = f"Voici les premiers : {texte_erreur} \n ..."
            facture.add_field(
                name=f"<:8056engagedinsuspectedspamactiv:1406904855536074823>  {len(liste_erreurs)} blocs inconnus (comptés à 0$)",
                value=message_erreur, inline=False)

        view_bouton = BoutonExcel(nom_propre, count, donnees_totale, donnees_prix)
        await interaction.followup.send(embed=facture, view=view_bouton)

    except Exception as e:
        await interaction.followup.send(f"⚠️ Une erreur inattendue est survenue : {e}")
    finally:
        if os.path.exists(chemin_local):
            os.remove(chemin_local)
if __name__ == "__main__":
    f = open('token.txt', 'r')
    bot.run(f.read().strip())
    f.close()