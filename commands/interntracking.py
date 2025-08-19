import discord
from discord import app_commands, Interaction, Object
import os
import PyPDF2
import io
import aiohttp
from dotenv import load_dotenv

load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"


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
        
    @tree.command(name="resumereview", description="Upload your resume PDF for AI feedback", guild=Object(id=guild_id))
    async def resumereview(interaction: Interaction, file: discord.Attachment):
        await interaction.response.defer(thinking=True)
        if not file.filename.lower().endswith(".pdf"):
            await interaction.followup.send("Please upload a PDF file.", ephemeral=True)
            return
        # Download the PDF
        async with aiohttp.ClientSession() as session:
            async with session.get(file.url) as resp:
                if resp.status != 200:
                    await interaction.followup.send("Failed to download the PDF.", ephemeral=True)
                    return
                pdf_bytes = await resp.read()
        # Extract text from PDF
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            await interaction.followup.send(f"Failed to read PDF: {e}", ephemeral=True)
            return
        if not text.strip():
            await interaction.followup.send("Could not extract any text from the PDF.", ephemeral=True)
            return
        # Send to GPT
        prompt = f"You are a professional resume reviewer. Give concise, actionable feedback for this resume:\n\n{text[:3500]}"
        url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 500}}

        print(HF_API_KEY)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    err = await resp.text()
                    await interaction.followup.send(f"Hugging Face API error: {err}", ephemeral=True)
                    return
                result = await resp.json()
        # Hugging Face sometimes returns a list
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            review = result[0]["generated_text"].strip()
        else:
            review = str(result)

        await interaction.followup.send(f"**Resume Review:**\n{review}")