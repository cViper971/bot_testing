import discord

def setup_interntracking_commands(tree, guild_id, role_name):
    @tree.command(name="getinternrole", description="Get notified for new internship postings.", guild=discord.Object(id=guild_id))
    async def get_intern_role(interaction: discord.Interaction):
        guild = interaction.guild
        member = interaction.user
        # Find or create the role
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            try:
                role = await guild.create_role(name=role_name, mentionable=True, reason="Internship notification role")
            except Exception as e:
                await interaction.response.send_message(f"Failed to create role: {e}", ephemeral=True)
                return
        # Add role to user
        try:
            await member.add_roles(role, reason="Opt-in for internship notifications")
            await interaction.response.send_message(f"You now have the {role.mention} role and will be notified for new internships!", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to add role: {e}", ephemeral=True)