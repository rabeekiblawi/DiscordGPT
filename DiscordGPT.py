import discord
from discord.ext import commands
import openai
import os
from discord import Intents
from discord import app_commands
from config import TOKEN, OPENAI_API_KEY  # Add this line to import tokens

openai.api_key = OPENAI_API_KEY
intents = Intents.default()
intents.typing = False
intents.presences = True
intents.members = True

client = commands.Bot(command_prefix='d!', intents=intents)

@client.event
async def on_ready():
    print("Bot is Up and Ready!")
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send('pong')


@client.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True
    )

@client.tree.command(name="say")
@app_commands.describe(things_to_say="What should I say?")
async def say(interaction: discord.Interaction, things_to_say: str):
    await interaction.response.send_message(f"{interaction.user.name} said: '{things_to_say}'")

client.run(TOKEN)