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
            await ctx.message.channel.send("Gold Guerilla Match notifications will now be **disabled** for channel '{}'.".format(ctx.message.channel))
        else:
            notify_gold.append(ctx.message.channel.id)
            await ctx.message.channel.send("Gold Guerilla Match notifications will now be **enabled** for channel '{}'.".format(ctx.message.channel))
    
    @commands.command(pass_context=True)
    async def print(self, ctx):
        await self.bot.wait_until_ready()
        global current_time
        local_time = "http://worldtimeapi.org/api/timezone/Australia/Brisbane"
        data = requests.get(local_time)
        date_time = data.json()
        get_time = date_time["datetime"]
        start = get_time.find("T") + 1
        end = get_time.find(":", start)
        thetime = get_time[start:end]
        
        await ctx.message.channel.send("The Time is: {} and the 'current time': {}".format(thetime, current_time))

    
    @tasks.loop(seconds=10.0)
    async def check_time(self):
        global current_time
        local_time = "http://worldtimeapi.org/api/timezone/Australia/Brisbane"
        data = requests.get(local_time)
        date_time = data.json()

        notify_time = ["00", "06", "12", "18"]

        if date_time["day_of_week"] > 0 and date_time["day_of_week"] < 6:
            get_time = date_time["datetime"]
            start = get_time.find("T") + 1
            end = get_time.find(":", start)
            thetime = get_time[start:end]
            print("check0")
            if thetime in notify_time:
                print("check1")
                for server in notify_gold:
                    print("check2")
                    if current_time == thetime:
                        print("check_break")
                        break
                    print("check3")
                    channel = self.bot.get_channel(server)
                    await channel.send("Gold Guerilla Match has started!")
                    current_time = thetime
                    print("check4")
                    
    @check_time.before_loop
    async def before_check(self):
        print('waiting...')
        await self.bot.wait_until_ready()
                

def setup(bot):
    bot.add_cog(Gold(bot))
