import feedparser
import asyncio
import discord

last_commit_id = None  # Global variable to cache last seen commit

async def check_github_commits(client: discord.Client, channel_id: int, user_id: int, repo_url: str, interval: int = 300):
    global last_commit_id
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    feed_url = f"https://github.com/{repo_url}/commits/master.atom"

    while not client.is_closed():
        feed = feedparser.parse(feed_url)
        if feed.entries:
            print(feed.entries)
            latest = feed.entries[0]
            if latest.id != last_commit_id:
                last_commit_id = latest.id
                message = (
                    f"🛠️ New commit in **{feed.feed.title}**:\n"
                    f"**{latest.title}**\n"
                    f"<{latest.link}>\n"
                    f"<@{user_id}>"
                )
                await channel.send(message)
        await asyncio.sleep(interval)