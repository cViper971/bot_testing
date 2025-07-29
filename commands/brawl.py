from discord import app_commands, Interaction, Object
import os
from utils import brawl

def setup_brawl_commands(tree, GUILD_ID):
    @tree.command(name="player_stats", description="Get your Brawl Stars stats", guild=Object(id=GUILD_ID))
    async def player_stats(interaction: Interaction):
        user_id = str(interaction.user.id)
        tag = brawl.player_tags.get(user_id)
        if not tag:
            await interaction.response.send_message("You haven’t set your player tag yet. Use `/set_id` first.")
            return

        data = brawl.get_player(tag)
        if data:
            name = data["name"]
            trophies = data["trophies"]
            await interaction.response.send_message(f"{name} has {trophies} trophies.")
        else:
            await interaction.response.send_message("Player not found or API error.")

    @tree.command(name="set_id", description="Save your Brawl Stars player tag", guild=Object(id=GUILD_ID))
    @app_commands.describe(tag="Your Brawl Stars tag (e.g. #ABCD1234)")
    async def set_id(interaction: Interaction, tag: str):
        user_id = str(interaction.user.id)
        brawl.player_tags[user_id] = tag.strip().upper()
        brawl.save_tags()
        await interaction.response.send_message(f"Your tag `{tag}` has been saved!")