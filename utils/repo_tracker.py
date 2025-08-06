import aiohttp
import asyncio
import discord
import json

last_seen_key = None

async def fetch_listings_json(repo_url: str):
    raw_url = f"https://raw.githubusercontent.com/{repo_url}/master/.github/scripts/listings.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(raw_url) as resp:
            if resp.status == 200:
                text = await resp.text()
                try:
                    return json.loads(text)
                except Exception as e:
                    print(f"Failed to parse listings.json: {e}")
    return None

async def check_github_commits(client: discord.Client, channel_id: int, user_id: int, repo_url: str, interval: int = 300):
    global last_seen_key
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    while not client.is_closed():
        listings = await fetch_listings_json(repo_url)
        if listings and len(listings) > 0:
            new_entries = []
            for entry in listings:
                key = f"{entry.get('company','').strip()}::{entry.get('title','').strip()}"
                if last_seen_key is None:
                    last_seen_key = key
                    break
                if key == last_seen_key:
                    break
                if(entry.get("season") == "Summer"):
                    new_entries.append(entry)
            if new_entries:
                for entry in reversed(new_entries):
                    company = entry.get('company_name', 'Unknown Company')
                    title = entry.get('title', 'Unknown Title')
                    message = f"<@{user_id}> New internship: **{company}** - **{title}**"
                    await channel.send(message)
                last_seen_key = f"{listings[0].get('company','').strip()}::{listings[0].get('title','').strip()}"
        await asyncio.sleep(interval)