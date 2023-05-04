# to create a slash command in discord bots you need to follow the following convention:
#@client.tree.command(name="example command")
#to add description use this : @app_commands.describe(example description")
#to add interaction use this: interaction: discord.Interaction, things_to_say: str. 

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

async def generate_text(prompt: str) -> str:
    model_engine = "text-davinci-002"

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    generated_text = response.choices[0].text.strip()
    return generated_text

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

@client.tree.command(name="generate")
@app_commands.describe(prompt="What should ChatGPT generate?")
async def generate(interaction: discord.Interaction, prompt: str):
    try:
        generated_text = await generate_text(prompt)
        await interaction.response.send_message(f"ChatGPT generated: '{generated_text}'", ephemeral=True)
    except Exception as e:
        print(f"Error in generate command: {e}")
        await interaction.response.send_message("An error occurred while generating text. Please try again.", ephemeral=True)

client.run(TOKEN)
