from discord.ext import commands
import openai
from dotenv import load_dotenv
import os

load_dotenv()

async def setup(bot):
    await bot.add_cog(TestCmds(bot))

class TestCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = os.getenv("OPENAI_KEY")

    @commands.command(name="hello")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def AskGPT(self, ctx, *args):
        print("meow")
        await ctx.message.channel.send("Hello World!")

    @commands.command(name="ask")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def AskGPT(self, ctx, *args):
        prompt = " ".join(args)
        print(prompt)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(response)
        answer = response.choices[0].message.content.strip()
        await ctx.message.channel.send(answer)