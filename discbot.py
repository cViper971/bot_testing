import discord
from discord import app_commands
import os
from dotenv import load_dotenv
from utils.repo_tracker import check_github_commits

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

INTERNSHIP_ROLE_NAME = "Internship Alerts"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Function to load commands
def load_commands():
    from commands.general import setup_general_commands
    from commands.brawl import setup_brawl_commands
    from commands.interntracking import setup_interntracking_commands
    
    setup_general_commands(tree, GUILD_ID)
    setup_brawl_commands(tree, GUILD_ID)
    setup_interntracking_commands(tree, GUILD_ID, INTERNSHIP_ROLE_NAME)

@client.event
async def on_ready():
    load_commands()
    try:
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    client.loop.create_task(
        check_github_commits(
            client=client,
            channel_id=1370506707494764671,
            role_name=INTERNSHIP_ROLE_NAME,
            repo_url="vanshb03/Summer2026-Internships",
            interval=120
        )
    )

client.run(DISCORD_TOKEN)