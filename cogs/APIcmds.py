import discord
import json
from discord.ext import commands
import add_ons.epic7API as e7API
import add_ons.ss_CMDS as ssCMDS
import add_ons.al_CMDS as alCMDS

colours = {
    "Fire": 0xff3535,
    "Earth": 0x4ee031,
    "Ice": 0x38cef7,
    "Dark": 0x815bff,
    "Light": 0xffff30
}

SS_colours = {
    "F6CECE": 0xF6CECE,
    "A9F5A9": 0xA9F5A9,
    "A9D0F5": 0xA9D0F5,
    "F3F781": 0xF3F781,
    "6A0888": 0x6A0888,
    "D0A9F5": 0xD0A9F5
}

SS_colours2 = {
    "ardor": 0xF6CECE,
    "whirlwind": 0xA9F5A9,
    "thunder": 0xA9D0F5,
    "light": 0xF3F781,
    "dark": 0xD0A9F5
}

AL_colours = {
    "Common": 0xB9B9B9,
    "Rare": 0x91DFFF,
    "Elite": 0x8050FF,
    "Super Rare": 0xFFE349
}


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

    #  Epic Seven
    @commands.command(pass_context=True, aliases=["epic7"])
    async def e7(self, ctx, *, mes=""):
        if mes == "":
            reply = discord.Embed(title="Epic Seven Commands:",
                                  description="Please use any of these commands followed by ';e7' to search.\n **For an example:** `.e7 Hero Angelica`",
                                  color=0x03a1fc)
            reply.add_field(name="Latest", value="\t Returns the latest heroes and artifacts.", inline=False)
            reply.add_field(name="Hero <name>", value="\t Returns information about that hero.", inline=False)
            reply.add_field(name="Skills <name>", value="\t Returns that hero's skillset.", inline=False)
            reply.add_field(name="Artifact <name>", value="\t Returns information about that artifact.", inline=False)
            reply.add_field(name="Item <name>", value="\t Returns information about that item.", inline=False)
            await ctx.message.channel.send(embed=reply)

        elif mes.lower() == "latest":
            get_latest = e7API.get_latest()
            reply = discord.Embed(title="Latest Epic Seven Heroes and Artifacts",
                                  description=" ",
                                  color=0x03a1fc)
            for keytype in get_latest["results"][0].keys():
                for info in get_latest["results"][0][keytype]:
                    #  info = info.replace("-", " ")  # replaces the blank space with a "-"
                    if keytype == "hero":
                        reply.add_field(name="[{}] {}".format("Hero", info["name"]), value="Rarity: {}★\n"
                                                                                           "Class: {} \n"
                                                                                           "Element: {} \n"
                                                                                           "Zodiac: {}".format(
                            info["rarity"], info["classType"].capitalize(), info["element"].capitalize(),
                            info["zodiac"].capitalize()), inline=False)
                    elif keytype == "artifact":
                        exclusive = info["exclusive"]
                        if exclusive == []:
                            exclusive = ["None"]
                        reply.add_field(name="[{}] {}".format("Artifact", info["name"]), value="Rarity: {}★\n"

                                                                                               "Exclusive: {} \n".format(
                            info["rarity"], "".join(exclusive).capitalize()), inline=False)
            reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await ctx.message.channel.send(embed=reply)
            pass

        elif mes.lower().startswith("hero ") or mes.lower().startswith("char "):
            name = mes.lower().split(" ", maxsplit=1)[1]
            name = name.replace(" ", "-")  # replaces the blank space with a "-"
            try:
                get_hero = e7API.get_info(name, "hero")["results"][0]
            except KeyError:
                await ctx.message.channel.send(embed=HandleError.HandleType(self))
                return

            reply = discord.Embed(title="{}".format(get_hero["name"]),
                                  description="> {}★ | {} | {} | {}".format(get_hero["rarity"],
                                                                            get_hero["classType"].capitalize(),
                                                                            get_hero["element"].capitalize(),
                                                                            get_hero["zodiac"].capitalize()),
                                  color=colours[get_hero["element"].capitalize()])
            reply.set_thumbnail(url="https://assets.epicsevendb.com/{}/{}/icon.png".format("hero", name))
            reply.add_field(name="Story:", value=get_hero["background"], inline=False)
            reply.add_field(name="Stats (Level 1):", value="```\n"
                                                           "| HP: {} | ATK: {} | SPD: {} |\t\t\n"
                                                           "| DEF: {} | CHC: {} | CHD: {} |\t\t\n"
                                                           "| EFF: {} | EFR: {} | DAC: {} |\t\t\n```".format(
                get_hero["stats"]["lv1BaseStarNoAwaken"]["cp"], get_hero["stats"]["lv1BaseStarNoAwaken"]["atk"],
                get_hero["stats"]["lv1BaseStarNoAwaken"]["hp"],
                get_hero["stats"]["lv1BaseStarNoAwaken"]["spd"], get_hero["stats"]["lv1BaseStarNoAwaken"]["def"],
                get_hero["stats"]["lv1BaseStarNoAwaken"]["chc"],
                get_hero["stats"]["lv1BaseStarNoAwaken"]["chd"], get_hero["stats"]["lv1BaseStarNoAwaken"]["eff"],
                get_hero["stats"]["lv1BaseStarNoAwaken"]["efr"], get_hero["stats"]["lv1BaseStarNoAwaken"]["dac"]),
                            inline=False)

            reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await ctx.message.channel.send(embed=reply)

        elif mes.lower().startswith("skills ") or mes.lower().startswith("skill ") or mes.lower().startswith(
                "ability "):
            name = mes.lower().split(" ", maxsplit=1)[1]
            name = name.replace(" ", "-")  # replaces the blank space with a "-"
            try:
                get_hero = e7API.get_info(name, "hero")["results"][0]
            except:
                await ctx.message.channel.send(embed=HandleError.HandleType(self))
                return

            reply = discord.Embed(title="{}'s Skills".format(get_hero["name"]),
                                  description=" ",
                                  color=colours[get_hero["element"].capitalize()])
            for skill in get_hero["skills"]:
                skilltype = "Active"
                if skill["isPassive"]:
                    skilltype = "Passive"
                if skill["soulBurn"] > 0:
                    reply.add_field(name="({}) {}".format(skilltype, skill["name"]),
                                    value="> Cooldown: {} turns  \n {} \n```\nSoul Burn: {}\nEffect: {}```".format(
                                        skill["cooldown"], skill["description"], skill["soulBurn"],
                                        skill["soulBurnEffect"]), inline=False)
                else:
                    reply.add_field(name="({}) {}".format(skilltype, skill["name"]),
                                    value="> Cooldown: {} turns  \n {}".format(skill["cooldown"], skill["description"]),
                                    inline=False)
            reply.set_thumbnail(url="https://assets.epicsevendb.com/{}/{}/icon.png".format("hero", name))
            reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)

            await ctx.message.channel.send(embed=reply)

        elif mes.lower().startswith("artifact ") or mes.lower().startswith("arti "):
            name = mes.lower().split(" ", maxsplit=1)[1]
            name = name.replace(" ", "-")  # replaces the blank space with a "-"

            try:
                get_artifact = e7API.get_info(name, "artifact")["results"][0]
            except:
                await ctx.message.channel.send(embed=HandleError.HandleType(self))
                return

            lore = get_artifact["loreDescription"]
            lore_temp = ""
            for line in lore:
                lore_temp = lore_temp + line + "\n"
            reply = discord.Embed(title=get_artifact["name"],
                                  description="> {}★ | {} Exclusive".format(get_artifact["rarity"],
                                                                            get_artifact["exclusive"][0].capitalize()),
                                  color=0xff7300)
            reply.set_thumbnail(url="https://assets.epicsevendb.com/{}/{}/icon.png".format("artifact", name))
            reply.add_field(name="Lore:", value=lore_temp, inline=False)
            reply.add_field(name="Skills:",
                            value="**Level 1:** {}\n **Maxed:** {}".format(get_artifact["skillDescription"]["base"],
                                                                           get_artifact["skillDescription"]["max"]),
                            inline=False)
            reply.add_field(name="Stats (Level 1):",
                            value="ATK: {}\n HP: {}".format(get_artifact["stats"]["base"]["atk"],
                                                            get_artifact["stats"]["base"]["hp"]), inline=False)
            reply.add_field(name="Stats (Max):", value="ATK: {}\n HP: {}".format(get_artifact["stats"]["max"]["atk"],
                                                                                 get_artifact["stats"]["max"]["hp"]))
            reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await ctx.message.channel.send(embed=reply)
            pass

        elif mes.lower().startswith("item "):
            name = mes.lower().split(" ", maxsplit=1)[1]
            name = name.replace(" ", "-")  # replaces the blank space with a "-"

            try:
                get_item = e7API.get_info(name, "item")["results"][0]
            except:
                await ctx.message.channel.send(embed=HandleError.HandleType(self))
                return

            shopItems = "\u200b"
            droplocations = "\u200b"

            if "apShops" in get_item:
                shopItems = ""
                for shop in get_item["apShops"]:
                    shopItems += "**{}:** ${} | x{}\n".format(shop["chapter"], shop["cost"], shop["quantity"])

            if get_item["locations"] != []:
                droplocations = ""
                for area in get_item["locations"]:
                    droplocations += "**Node:** {} \n**Name: **{} \n **Mob count:** {}\n\n".format(area["node"],
                                                                                                   area["name"],
                                                                                                   area["mobcount"])

            reply = discord.Embed(title=get_item["name"],
                                  description=get_item["type"].capitalize(),
                                  color=0x6a38ff)
            reply.set_thumbnail(url="https://assets.epicsevendb.com/{}/{}.png".format("item", name))
            reply.add_field(name="Description:", value=get_item["description"], inline=False)
            reply.add_field(name="Locations:", value=droplocations, inline=False)
            reply.add_field(name="AP Shops:", value=shopItems, inline=False)
            reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)

            await ctx.message.channel.send(embed=reply)

    #  Soccer Spirits
    @commands.command(pass_context=True, aliases=["soccerspirits"])
    async def ss(self, ctx, *, mes=""):
        if mes == "":
            reply = discord.Embed(title="Soccer Spirits Commands:",
                                  description="Please use any of these commands followed by ';ss' to search.\n **For an example:** `;ss tw Miri: Miri is wondering`",
                                  color=0x03a1fc)
            reply.add_field(name="Tw <player>: <sentence>",
                            value="Returns the teamwork of the given player. The full teamwork sentence does not have to be entered.",
                            inline=False)
            reply.add_field(name="Player <name>",
                            value="Returns information about the player. (Work in progress. Only works for legends as of now)",
                            inline=False)
            reply.add_field(name="Skills <player>",
                            value="Returns the skills of the player. (Work in progress. Only works for legends as of now)",
                            inline=False)
            reply.add_field(name="UQ <stone>", value="Returns the effects of the unique stone.", inline=False)
            reply.add_field(name="DR <value> <value> <value>..",
                            value="Calculates the DR from the given values. Please enter the values as integers.",
                            inline=False)
            await ctx.message.channel.send(embed=reply)
        if mes.lower().startswith("tw ") or mes.lower().startswith("teamwork "):
            try:
                content = mes.lower().split(" ", maxsplit=1)[1]
                player = content.split(":", maxsplit=1)[0].strip()
                question = content.split(":", maxsplit=1)[1].strip()

                get_teamwork = ssCMDS.get_teamwork(player, question)

                reply = discord.Embed(title="{} Teamwork".format(get_teamwork[0]),
                                      description="**Question:** {}\n\n **Answer:** {}".format(get_teamwork[1],
                                                                                               get_teamwork[2]),
                                      color=0x5cffbe)
                reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)

                await ctx.message.channel.send(embed=reply)
            except:
                reply = discord.Embed(title="Error",
                                      description="Please use the proper format\n\nExample: `;ss tw Miri: Miri is wondering`",
                                      color=0x5cffbe)
                reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)

                await ctx.message.channel.send(embed=reply)

        if mes.lower().startswith("uq ") or mes.lower().startswith("unique "):
            try:
                content = mes.lower().split(" ", maxsplit=1)[1]
                get_stone = ssCMDS.get_UQ(content)
                if get_stone == "empty":
                    await ctx.message.channel.send(embed=HandleError.HandleType(self))
                    return

                reply = discord.Embed(title=get_stone[0],
                                      description="{}\n {} \n > **Legendary:** {}".format(get_stone[3], get_stone[4],
                                                                                          get_stone[5]),
                                      color=SS_colours[get_stone[1]])
                reply.set_thumbnail(url=get_stone[2])
                reply.set_author(name="Unique Stone")
                reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await ctx.message.channel.send(embed=reply)
            except:
                reply = discord.Embed(title="Error",
                                      description="Please use the proper format\n\nExample: `;ss uq EBM`",
                                      color=0x5cffbe)
                reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await ctx.message.channel.send(embed=reply)
        if mes.lower().startswith("player ") or mes.lower().startswith("character ") or mes.lower().startswith("char "):
            try:
                content = mes.lower().split(" ", maxsplit=1)[1]
                get_player = ssCMDS.get_player(content, "player")
                if get_player == {}:
                    await ctx.message.channel.send(embed=HandleError.HandleType(self))
                    return
                reply = discord.Embed(title=get_player["name"],
                                      description="> {}★ | {} | {}\n".format(get_player["rarity"],
                                                                             get_player["gender"].capitalize(),
                                                                             get_player["element"].capitalize()),
                                      color=SS_colours2[get_player["element"]])

                reply.set_thumbnail(url=get_player["icon"])
                reply.add_field(name="Role", value=get_player["role"])
                reply.add_field(name="Immunity", value=get_player["immunity"])
                reply.add_field(name="Stone slots", value=get_player["stones"])
                reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await ctx.message.channel.send(embed=reply)
            except:
                reply = discord.Embed(title="Error",
                                      description="Please use the proper format\n\nExample: `;ss player dalgi`",
                                      color=0x5cffbe)
                reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await ctx.message.channel.send(embed=reply)
        if mes.lower().startswith("skills ") or mes.lower().startswith("skill "):
            try:
                content = mes.lower().split(" ", maxsplit=1)[1]
                get_player = ssCMDS.get_player(content, "skills")
                if get_player == {}:
                    await ctx.message.channel.send(embed=HandleError.HandleType(self))
                    return
                reply = discord.Embed(title="{}'s Skills".format(get_player["name"]),
                                      description=" ",
                                      color=SS_colours2[get_player["element"]])

                reply.set_thumbnail(url=get_player["icon"])
                reply.add_field(name="Ace", value=get_player["skills"][0]["description"], inline=False)
                reply.add_field(name="Active", value=get_player["skills"][1]["description"], inline=False)
                reply.add_field(name="Passive", value=get_player["skills"][2]["description"], inline=False)
                reply.add_field(name="Passive", value=get_player["skills"][3]["description"], inline=False)
                reply.add_field(name="Passive", value=get_player["skills"][4]["description"], inline=False)
                reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await ctx.message.channel.send(embed=reply)
            except:
                reply = discord.Embed(title="Error",
                                      description="Please use the proper format\n\nExample: `;ss skills lif`",
                                      color=0x5cffbe)
                reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await ctx.message.channel.send(embed=reply)
        if mes.lower().startswith("dr ") or mes.lower().startswith("damagereduction "):
            try:
                content = mes.lower().split(" ", maxsplit=1)[1]
                values = content.split(" ")
                dr_total = 0
                for index in range(len(values)):
                    if index == 0:
                        dr_total = 1 - (int(values[index]) / 100)
                    else:
                        dr_total = dr_total * (1 - (int(values[index]) / 100))
                dr_total = 1 - dr_total
                dr_total = round(dr_total * 100, 2)
                reply = discord.Embed(title="Soccer Spirits Damage Reduction Calculator",
                                      description="> {}\n**Damage Reduction:** {}%".format(values, dr_total),
                                      color=0x5cffbe)
                reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await ctx.message.channel.send(embed=reply)
            except:
                reply = discord.Embed(title="Error",
                                      description="Please use the proper format\n\nExample: `;ss dr 30 45 15`",
                                      color=0x5cffbe)
                reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await ctx.message.channel.send(embed=reply)

    @commands.command(pass_context=True, aliases=["azurlane"])
    async def al(self, ctx, *, mes=""):
        if mes == "":
            reply = discord.Embed(title="Azur Lane Commands:",
                                  description="Please use any of these commands followed by ';al' to search.\n **For an example:** `;al ship Enterprise`",
                                  color=0x03a1fc)
            reply.add_field(name="ship <name>",
                            value="Returns information about that ship.",
                            inline=False)
            reply.add_field(name="skins <ship>: <skin>",
                            value="Returns the skin names for that ship.",
                            inline=False)
            await ctx.message.channel.send(embed=reply)
        if mes.lower().startswith("ship ") or mes.lower().startswith("unit "):
            content = mes.lower().split(" ", maxsplit=1)[1]
            al_data = alCMDS.get_ship(content)
            if al_data["statusCode"] != 200:
                await ctx.message.channel.send(embed=HandleError.HandleType(self))
                return
            skin_string = ""
            reply = discord.Embed(
                title="{} {}".format(al_data["ship"]["nationalityShort"], al_data["ship"]["names"]["en"]),
                description="> {} | {}".format(al_data["ship"]["stars"]["value"], al_data["ship"]["rarity"]),
                color=AL_colours[al_data["ship"]["rarity"]])
            reply.add_field(name="Other names:",
                            value="**cn:** {};  **jp:** {};  **kr:** {}".format(al_data["ship"]["names"]["cn"],
                                                                                al_data["ship"]["names"]["jp"],
                                                                                al_data["ship"]["names"]["kr"]),
                            inline=False)
            reply.add_field(name="Classification:", value=al_data["ship"]["hullType"])
            reply.add_field(name="Class:", value=al_data["ship"]["class"])
            reply.add_field(name="Nationality:", value=al_data["ship"]["nationality"])
            reply.add_field(name="Build time:", value=al_data["ship"]["buildTime"])

            for skin in al_data["ship"]["skins"]:
                skin_string += "{}, ".format(skin["title"])

            reply.add_field(name="Skins:", value=skin_string)
            reply.set_thumbnail(url=al_data["ship"]["thumbnail"])
            reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
            await ctx.message.channel.send(embed=reply)
        if mes.lower().startswith("skin ") or mes.lower().startswith("skins "):
            content = mes.lower().split(" ", maxsplit=1)[1]
            try:
                ship = content.lower().split(": ", maxsplit=1)[0]
                skin = content.lower().split(": ", maxsplit=1)[1]
                al_data = alCMDS.get_ship(ship)
                if al_data["statusCode"] != 200:
                    await ctx.message.channel.send(embed=HandleError.HandleType(self))
                    return
                for ship_skin in al_data["ship"]["skins"]:
                    if skin in ship_skin["title"].lower():
                        reply = discord.Embed(
                            title="{} {}".format(al_data["ship"]["nationalityShort"], al_data["ship"]["names"]["en"]),
                            description=ship_skin["title"], color=AL_colours[al_data["ship"]["rarity"]])
                        reply.set_image(url=ship_skin["image"])
                        reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                        await ctx.message.channel.send(embed=reply)
                        return
                await ctx.message.channel.send(embed=HandleError.HandleType(self))
                return
            except:
                reply = discord.Embed(title="Error",
                                      description="Please use the proper format\n\nExample: `;al skin Akagi: Paradise`",
                                      color=0x5cffbe)
                reply.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
                await ctx.message.channel.send(embed=reply)


def setup(bot):
    bot.add_cog(MainCommands(bot))
