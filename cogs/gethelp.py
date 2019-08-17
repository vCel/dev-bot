import discord
from discord.ext import commands


class MainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["h", "bangwo", "tasukete"])
    async def help(self, ctx):
        embed = discord.Embed(description="To use me, please use the ';' prefix followed by any of the commands listed below.\n"
                                          ""
                                          "```asciidoc\n"
                                          "= General Commands =\n\n"
                                          "help :: Displays this message.\n"
                                          "info :: Displays information about this bot.\n"
                                          "coin :: Flips a coin for when you can't decide on something.\n"
                                          "pick <a>, <b>.. :: Decides on a random option given.\n"
                                          "poll <question>: <a>, <b>.. :: Starts a poll with entered options.\n"
                                          "f :: For times when you need to pay respect.\n"
                                          "\n= Search from an API =\n\n"
                                          "anime <name> :: Searches an anime from MyAnimeList. (Incomplete until MAL API is back up)\n"
                                          "manga <name> :: Searches a manga from MyAnimeList. (Incomplete until MAL API is back up)\n"
                                          "e7 :: Look up information regarding the mobile game 'Epic 7' (Heroes, Artifacts, Items).\n"
                                          "ss :: Looks up information regarding the mobile game 'Soccer Spirits' (Teamwork).\n"
                                          "\n= Set reminders =\n\n"
                                          "ng :: Enables/Disables notifications in your current channel about Gold Guerilla Matches in 'Soccer Spirits'. (admin)```",

                              color=0x39fc03)
        embed.set_author(name="Nezuko Help")
        #await self.bot.send_message(ctx.message.author, embed=embed)
        await ctx.message.author.send(embed=embed)
        reply = discord.Embed(title="Help Sent!",
                              description="A Direct Message with the list of commands has been sent to you.",
                              color=0x39fc03)
        reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        await ctx.message.channel.send(embed=reply)


def setup(bot):
    bot.add_cog(MainCommands(bot))
