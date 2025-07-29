import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

PLAYER_FILE = "players.json"
BRAWL_API_TOKEN = os.getenv("BRAWL_API_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {BRAWL_API_TOKEN}"
}

# Load player tags from file
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
    return response.json() if response.status_code == 200 else None
