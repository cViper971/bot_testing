from discord import Interaction, Object

def setup_general_commands(tree, guild_id):
    @tree.command(name="hello", description="Say hello back!", guild=Object(id=guild_id))
    async def hello(interaction: Interaction):
        await interaction.response.send_message("Hello!")
    
    @tree.command(name="ping", description="Check bot latency", guild=Object(id=guild_id))
    async def ping(interaction: Interaction):
        latency = round(interaction.client.latency * 1000)
        await interaction.response.send_message(f"Pong! {latency}ms")