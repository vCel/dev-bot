import discord
from discord.ext import commands


class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower().startswith("wha-") and not message.author.bot:
            await message.channel.send("Wha-")
        if "uwu" in message.content.lower() and not message.author.bot:
            await message.channel.send("uwu")
        if message.content.lower().startswith("owo") and not message.author.bot:
            await message.channel.send("*W-what's this*")
            
            

def setup(bot):
    bot.add_cog(Responses(bot))
