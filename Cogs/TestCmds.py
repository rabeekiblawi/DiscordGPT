from discord.ext import commands
from dotenv import load_dotenv
import openai
import json
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
        await ctx.message.channel.send("Hello World!")

    @commands.command(name="ask")
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def AskGPT(self, ctx, *args):
        prompt = " ".join(args)
        newMessage = [{"role": "user", "content": prompt}]
        # print(ctx.message.author.id)
        userDB = open(f"./Makeshift-DB/{ctx.message.author.id}.json", "r+")
        try:
            chat = json.load(userDB) + newMessage
        except:
            chat = newMessage
        
        # print(chat)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chat
            )
            # print(response)
            answer = response.choices[0].message.content.strip()
            await ctx.message.channel.send(answer)
            chat += [response.choices[0].message]
            userDB.seek(0)
            json.dump(chat, userDB, indent=4)
            userDB.close()
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
