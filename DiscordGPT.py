import discord
from discord.ext import commands
import openai
import os

TOKEN = 'MTA5OTM2NDMyMzI3MDM0ODk1NA.G94_Lf.8OsNdDHJE70m4EDDnI1WMXfejFE_NxwCfEevio'
openai.api_key = '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'


intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online!')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, World!')


@bot.command()
async def ask(ctx, *, question: str):
    try:
        prompt = f"{question}\n\nAnswer:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        answer = response.choices[0].text.strip()
        await ctx.send(answer)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

bot.run(TOKEN)


@bot.command()
async def ask(ctx, *, question: str):
    try:
        prompt = f"{question}\n\nAnswer:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )
        answer = response.choices[0].text.strip()
        await ctx.send(answer)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

ß