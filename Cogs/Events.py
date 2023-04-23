from discord.ext import commands, tasks
import discord

async def setup(bot):
    await bot.add_cog(Events(bot))

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("ChatGPT-Bot Online!!")
        await self.DClient.change_presence(activity=discord.Game(f"Solving Life's Issues"))