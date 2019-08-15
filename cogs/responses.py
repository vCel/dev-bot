import discord
from discord.ext import commands


class Responses:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.content.lower().startswith("wha-") and not message.author.bot:
            await self.bot.send_message(message.channel, "Wha-")
        if message.content.lower().startswith("creeper") and not message.author.bot:
            await self.bot.send_message(message.channel, "Aww man")
        if "uwu" in message.content.lower() and not message.author.bot:
            await self.bot.send_message(message.channel, "uwu")
        if "owo" in message.content.lower() and not message.author.bot:
            await self.bot.send_message(message.channel, "*W-what's this*")


def setup(bot):
    bot.add_cog(Responses(bot))
