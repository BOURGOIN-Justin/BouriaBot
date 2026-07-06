import discord
from discord.ext import commands
from discord import app_commands

class ValidationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

@app_commands.command(name="validation", description="Permet de donner le rôle 'validé' sur le serveur discord")
@app_commands.describe(joueur="pseudo du joueur à valider")
@app_commands.checks.has_role(1497908971963551846)
async def validation(interaction: discord.Interaction, joueur: discord.Member):
    guild = interaction.guild
    role_valide = guild.get_role(1271510865627058273)

    if role_valide is None:
        await interaction.response.send_message("❌ Erreur critique : Le rôle **Validé** n'existe pas. Vérifiez l'ID !", ephemeral=True)
        return

    if role_valide in joueur.roles:
        await interaction.response.send_message(f"⚠️ {joueur.mention} possède déjà le rôle Validé !", ephemeral=True)
        return

    await joueur.add_roles(role_valide)
    await interaction.response.send_message(f"Le joueur **{joueur.mention}** est désormais validé !")

@validation.error
async def validation_erreur(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingRole):
        await interaction.response.send_message("❌ Accès refusé : Seul un Dirigeant peut valider les nouveaux joueurs !", ephemeral=True)
    else:
        await interaction.response.send_message("⚠️ Une erreur est survenue lors de la validation.", ephemeral=True)
        print(f"Erreur commande validation : {error}")

async def setup(bot):
    await bot.add_cog(ValidationCog(bot))