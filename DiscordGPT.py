from discord.ext import commands
from dotenv import load_dotenv
import discord
import openai
import os
import asyncio

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="-", case_insensitive=True, intents=intents)

async def loadExt():
    async with bot:
        await bot.load_extension("Cogs.TestCmds")
        await bot.load_extension("Cogs.Events")
        await bot.start(TOKEN)

asyncio.run(loadExt())
