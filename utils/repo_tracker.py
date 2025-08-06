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
            if last_commit_id is None:
                last_commit_id = feed.entries[0].id

            commits_to_send = []
            for entry in feed.entries:
                if entry.id == last_commit_id:
                    break
                commits_to_send.append(entry)

            if commits_to_send:
                for commit in reversed(commits_to_send):
                    message = (
                        f"🛠️ New commit in **{feed.feed.title}**:\n"
                        f"**{commit.title}**\n"
                        f"<{commit.link}>\n"
                        f"<@{user_id}>"
                    )
                    await channel.send(message)

                last_commit_id = commits_to_send[0].id
        
        await asyncio.sleep(interval)