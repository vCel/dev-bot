import discord
import os
from discord.ext import commands

command_prefix = ";"
description = "UwU"
bot = commands.Bot(command_prefix=command_prefix, description=description)

TOKEN = os.getenv('TOKEN')

cogs = ["cogs.APIcmds", "cogs.generalcmds", "cogs.responses", "cogs.gethelp"]


class NezukoBot:
    def __int__(self, bot):
        self.bot = bot

    @bot.event
    async def on_ready():
        print("Bot Status: Online \n"
              "Bot Name: {} \n"
              "Bot ID: {} \n"
              "Discord Version: {} \n"
              "==================="
              .format(bot.user.name, bot.user.id, discord.__version__))
        await bot.change_presence(game=discord.Game(name="h-hewwo | {}help".format(command_prefix)))

    bot.remove_command('help')


if __name__ == "__main__":
    for cog in cogs:
        bot.load_extension(cog)
    bot.run("NjA2MzMxNDAxMTA4NzE3NTcw.XUJhVw.WmKdJ7Sv7lUU4QMofMIpi5fAxSE")
