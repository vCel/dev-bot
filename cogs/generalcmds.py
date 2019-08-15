import discord
import json
from discord.ext import commands
from random import randint

poll_emojis = ["1\u20e3", "2\u20e3", "3\u20e3", "4\u20e3", "5\u20e3", "6\u20e3", "7\u20e3", "8\u20e3", "9\u20e3", "10\u20e3"]


class HandleError(commands.Cog):

    def HandleType(self):
        reply = discord.Embed(title="No results.",
                              description="Please ensure that the name you have entered is correct.",
                              color=0xff2bb1)
        reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        return reply


class MainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def info(self, ctx):
        owner_info = await self.bot.get_user_info("159194897855807488")
        reply = discord.Embed(title="Nezuko Information (´｡• ᵕ •｡`)", description="I am a bot made by **{}**. :)".format(owner_info),
                              color=0xffffff)
        await ctx.message.channel.send(embed=reply)

    @commands.command(pass_context=True, aliases=["F"])
    async def f(self, ctx):
        reply = discord.Embed(description="**{}** has paid their respect.".format(ctx.message.author.name),
                              color=0xffffff)
        await ctx.message.channel.send(embed=reply)

    @commands.command(pass_context=True, aliases=["flip"])
    async def coin(self, ctx):
        side = "Heads"
        randomint = randint(0, 100)
        if randomint > 50:
            side = "Tails"
        reply = discord.Embed(description="The coin landed on {}.".format(side),
                              color=0xffffff)
        reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.message.channel.send(embed=reply)

    @commands.command(pass_context=True, aliases=["choose"])
    async def pick(self, ctx, *, value=""):
        answer = "Please enter options."
        if value=="":
            reply = discord.Embed(description="{}".format(answer),
                                  color=0xffffff)
            await ctx.message.channel.send(embed=reply)
            return
        value = value.split(",")
        answer = value[randint(0, len(value) - 1)]
        await ctx.message.channel.send("I pick **{}**! o(>< )o".format(answer))

    @commands.command(pass_context=True)
    async def poll(self, ctx, *, value=""):
        box = ""
        if value == "":
            reply = discord.Embed(description="Please enter at least one option. (・`ω´・)",
                                  color=0x2effe7)
            await ctx.message.channel.send(embed=reply)
            return

        try:
            split_value = value.split(": ", maxsplit=1)
            value = split_value[1].split(",")
        except:
            return

        if len(value) > 9:
            reply = discord.Embed(description="You may only have up to 9 options... (・`ω´・)",
                                  color=0x2effe7)
            await ctx.message.channel.send(embed=reply)
            return

        for i, option in enumerate(value):
            new_emoji = emoji="{}\u20e3".format(i + 1)
            box += "{} {}.\n".format(new_emoji, option)

        reply = discord.Embed(title=split_value[0],
                              description=box,
                              color=0x2effe7)
        reply.set_author(name="{}'s Poll".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        msg = await ctx.message.channel.send(embed=reply)
        for length in range(len(value)):
            await ctx.message.add_reaction(emoji="{}\u20e3".format(length + 1))


def setup(bot):
    bot.add_cog(MainCommands(bot))
