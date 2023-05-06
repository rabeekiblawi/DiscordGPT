
import discord
from discord.ext import commands
import openai
import os
from discord import Intents
from discord import app_commands
from config import TOKEN, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
intents = Intents.default()
intents.typing = False
intents.presences = True
intents.members = True

client = commands.Bot(command_prefix='d!', intents=intents)

current_model_engine = "text-davinci-002"

async def generate_text(prompt: str, model_engine: str) -> str:
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


@client.tree.command(name="chat")
async def generate(
    interaction: discord.Interaction,
    prompt: str,
):
    try:
        await interaction.response.defer(ephemeral=True)

        global current_model_engine
        generated_text = await generate_text(prompt, current_model_engine)

        await interaction.followup.send(
            f"ChatGPT generated: '{generated_text}'", ephemeral=True
        )
    except Exception as e:
        print(f"Error in generate command: {e}")
        if not interaction.response.is_done():
            await interaction.followup.send(
                "An error occurred while generating text. Please try again.",
                ephemeral=True,
            )

@client.tree.command(name="set_model")
async def set_model(
    interaction: discord.Interaction,
    model: str,
):
    try:
        await interaction.response.defer(ephemeral=True)

        global current_model_engine

        if model.lower() == "davinci":
            current_model_engine = "text-davinci-002"
        elif model.lower() == "curie":
            current_model_engine = "text-curie-001"
        elif model.lower() == "babbage":
            current_model_engine = "text-babbage-001"
        elif model.lower() == "ada":
            current_model_engine = "text-ada-001"
        else:
            raise ValueError("Invalid model name.")

        await interaction.followup.send(
            f"Model has been set to: '{current_model_engine}'", ephemeral=True
        )
    except Exception as e:
        print(f"Error in set_model command: {e}")
        if not interaction.response.is_done():
            await interaction.followup.send(
                "An error occurred while setting the model. Please try again with a valid model name.",
                ephemeral=True,
            )


@client.tree.command(name="help")
async def help_command(interaction: discord.Interaction):
    available_models = [
        "davinci",
        "curie",
        "babbage",
        "ada",
    ]
    model_options = ", ".join(available_models)
    
    help_message = (
        "Here are the available commands and their usage:\n"
        "\n"
        "/chat <prompt> - Chat with the AI model.\n"
        "\n"
        f"/set_model <model> - Set the AI model. Available models: {model_options}\n"
        "\n"
        "/available_models - Display the available models.\n"
        "\n"
        "/help - Show this help message."
    )
    
    await interaction.response.send_message(help_message, ephemeral=True)


client.run(TOKEN)
