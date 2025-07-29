import discord
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Function to load commands
def load_commands():
    from commands.general import setup_general_commands
    from commands.brawl import setup_brawl_commands
    
    setup_general_commands(tree, GUILD_ID)
    setup_brawl_commands(tree, GUILD_ID)

@client.event
async def on_ready():
    load_commands()
    try:
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
    except Exception as e:
        print(f"Failed to sync commands: {e}")

client.run(DISCORD_TOKEN)