import discord
from discord import app_commands
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
BRAWL_API_TOKEN = os.getenv("BRAWL_API_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
PLAYER_FILE = "players.json"

HEADERS = {
    "Authorization": f"Bearer {BRAWL_API_TOKEN}"
}

if os.path.exists(PLAYER_FILE):
    with open(PLAYER_FILE, "r") as f:
        player_tags = json.load(f)
else:
    player_tags = {}

def save_tags():
    with open(PLAYER_FILE, "w") as f:
        json.dump(player_tags, f)

def get_player(tag):
    tag = tag.strip("#").upper()
    url = f"https://api.brawlstars.com/v1/players/%23{tag}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# Setup client and command tree
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Sync commands on ready
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Bot ready as {client.user}")

# Slash command definition
@tree.command(
    name="hello",
    description="Say hello back!",
    guild=discord.Object(id=GUILD_ID)
)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

@tree.command(
    name="player_stats",
    description="get player stats",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(
    player_id='The first value you want to add something to',
)
async def get_stats(interaction: discord.Interaction, player_id: str):
    new_id = player_tags.get(str(interaction.user.id))
    data = get_player("#"+new_id)
    if data:
        name = data["name"]
        trophies = data["trophies"]
        await interaction.response.send_message(f"{name} has {trophies} trophies.")
    else:
        await interaction.response.send_message("Player not found.")

@tree.command(
    name="set_id",
    description="Save your Brawl Stars player tag",
    guild=discord.Object(id=GUILD_ID)
)
@app_commands.describe(
    tag='The first value you want to add something to',
)
async def set_id(interaction: discord.Interaction, tag: str):
    user_id = str(interaction.user.id)
    player_tags[user_id] = tag.strip().upper()
    save_tags()
    await interaction.response.send_message(f"Your tag `{tag}` has been saved!")

# Run the bot
client.run(DISCORD_TOKEN)
