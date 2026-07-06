import discord
from discord.ext import commands
from discord import app_commands

class AllianceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="liste_alliance", description="Génère la liste des pays de la CDE")
    @app_commands.checks.has_role(1497908971963551846)
    async def liste_alliance(self, interaction: discord.Interaction):
        ID_CHANNEL = 1498355809153716436
        await interaction.response.defer(ephemeral=True)

        try:
            salon = self.bot.get_channel(ID_CHANNEL) or await self.bot.fetch_channel(ID_CHANNEL)
            alliance = 'Cde'

            infos = await self.bot.get_alliance_details(alliance)

            if infos == "API_DOWN":
                await interaction.followup.send("❌ L'API Yoxo est actuellement en panne. Réessaie plus tard.")
                return

            if not infos:
                await interaction.followup.send(f"❌ L'alliance `{alliance}` est introuvable ou vide.")
                return

            # "bot.user" devient "self.bot.user"
            await salon.purge(limit=5, check=lambda m: m.author == self.bot.user or m.embeds)

            embed = discord.Embed(
                title=f"🌍 Alliance : **{alliance.upper()}**",
                color=discord.Color.gold(),
                description=f"Répartition des pays • Mis à jour <t:{infos['last_update']}:R> "
            )
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1309952577781239868/1504788121034686665/logo.png?ex=6a0842a5&is=6a06f125&hm=73c9dc3a8c269a8c1ca8c7c5c897c6f93f6fcd9f29e132e0e4f79d1795b82ad9&')

            texte_chefs = ""
            for item in infos["chefs"]:
                texte_chefs += f"**{item['pays']}** : `{item['chef']}`\n"
            embed.add_field(name = "👑 Pays Fondateurs", value=texte_chefs or "Aucun", inline=False)

            texte_membres = ""
            for item in infos["membres"]:
                texte_membres += f"**{item['pays']}** : `{item['chef']}`\n"

            if len(texte_membres) > 1024: texte_membres = texte_membres[:1000] + "..."

            embed.add_field(name="👥 Pays Membres", value=texte_membres or "Aucun", inline=False)

            texte_protectorats =""
            for item in infos["protectorats"]:
                texte_protectorats += f"**{item['pays']}** : `{item['chef']}`\n"

            if len(texte_protectorats) > 1024: texte_protectorats = texte_protectorats[:1000] + "..."
            embed.add_field(name="🛡️ Pays sous protectorat", value=texte_protectorats or "Aucun", inline=False)

            embed.set_footer(text=f"Données Yoxo V2 • Serveur Black")

            await salon.send(embed=embed)
            await interaction.followup.send(f"✅ Liste envoyée dans <#{ID_CHANNEL}> !")

        except Exception as e:
            print(f"Erreur commande : {e}")
            try:
                await interaction.followup.send(f"⚠️ Une erreur est survenue : {e}")
            except:
                pass # Interaction expirée

async def setup(bot):
    await bot.add_cog(AllianceCog(bot))