import discord
import requests
from discord.ext import commands, tasks

notify_gold = [560368910881521666]
current_time = "69"


class Gold(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_time.start()

    @commands.command(pass_context=True, aliases=["ng"])
    @commands.has_permissions(administrator=True, manage_messages=True)
    async def notifygold(self, ctx):
        if ctx.message.channel.id in notify_gold:
            notify_gold.remove(ctx.message.channel.id)
            await ctx.message.channel.send("Gold Guerilla Match notifications will now be **disabled** for channel {}.".format(ctx.message.channel))
        else:
            notify_gold.append(ctx.message.channel.id)
            await ctx.message.channel.send("Gold Guerilla Match notifications will now be **enabled** for channel {}.".format(ctx.message.channel))

    @tasks.loop(seconds=5.0)
    async def check_time(self):
        await self.bot.wait_until_ready()
        global current_time
        local_time = "http://worldtimeapi.org/api/timezone/Australia/Brisbane"
        data = requests.get(local_time)
        date_time = data.json()

        notify_time = ["00", "06", "12", "18"]

        print(notify_gold)
        if date_time["day_of_week"] < 6:
            get_time = date_time["datetime"]
            start = get_time.find("T") + 1
            end = get_time.find(":", start)
            thetime = get_time[start:end]

            if thetime in notify_time:
                for server in notify_gold:
                    if current_time == thetime:
                        break
                    current_time = thetime
                    channel = self.bot.get_channel(server)
                    await channel.send("Gold Guerilla Match is on!")


def setup(bot):
    bot.add_cog(Gold(bot))
