import requests
import re


def get_teamwork(player, question):
    url = "http://pastebin.com/raw/7ASXKFzQ"
    get_request = requests.get(url)
    content = get_request.text

    pattern = re.compile("\[(.+?)\]")
    unit = pattern.findall(content)

    status = 0
    current_pos = 0
    for match in unit:
        if player in match.lower():
            status = 1
            qStart = content.find("[" + match + "]", current_pos) + len(match) + 2
            qEnd = content.find("\n", qStart)
            current_pos = qEnd

            get_question = content[qStart:qEnd]
            if question in get_question.lower():
                aStart = content.find("\t", current_pos)
                aEnd = content.find("\n", aStart)
                get_answer = content[aStart:aEnd]
                return [match, get_question, get_answer]
        elif status == 1:
            return ["Error has occurred.", "Question not Found.", ""]
            break

    return ["Error has occurred.", "Player not Found.", ""]


def get_UQ(stone):
    url = "https://soccerspirits.fandom.com/wiki/Category:Unique_(Spirit_Stone)"
    key = '<div style="border-top-left-radius:3px; border-top-right-radius:3px; text-align:left;text-indent:5px; background:'
    get_request = requests.get(url)
    content = get_request.text

    counter = content.count(key)
    current_pos = 0

    for number in range(counter):
        findSection = content.find(key, current_pos)

        colour1 = content.find("#", findSection)
        colour2 = content.find(";", colour1)
        get_colour = content[colour1+1:colour2]

        name1 = content.find("<b>", colour2)
        name2 = content.find("</b>", name1)
        get_name = content[name1+3:name2]

        img1 = content.find('https://vignette.wikia.nocookie.net/soccerspirits/images/', name2)
        img2 = content.find('"', img1)
        get_img = content[img1:img2]

        effecta1 = content.find("<td> ", img2)
        effecta2 = content.find("</td></tr>", effecta1)
        get_effecta = content[effecta1+5:effecta2]

        effectb1 = content.find("<td> ", effecta2)
        effectb2 = content.find("</td></tr>", effectb1)
        get_effectb = content[effectb1+5:effectb2]


        leg_key = '</td><td style="margin:1px; padding:4px; background:#F8F8F8;"> <b>'
        legend1 = content.find(leg_key, effectb2)
        legend2 = content.find('</b>', legend1)
        get_legend = content[legend1+len(leg_key):legend2]

        current_pos = colour2
        #print(get_name)
        if stone in get_name.lower():
            return [get_name, get_colour, get_img, get_effecta, get_effectb, get_legend]

    return "empty"


def get_player(player, target):
    api = "https://raw.githubusercontent.com/vCel/SS_API/master/players.json"
    json_obj = requests.get(api)
    data = json_obj.json()

    return_list = {}

    for unit in data["players"]:
        if player in unit["name"].lower() or player in unit["alias"].lower():
            if target == "player":
                return_list = {
                    "name": unit["name"],
                    "gender": unit["gender"],
                    "icon": unit["icon"],
                    "role": unit["role"],
                    "element": unit["element"],
                    "immunity": unit["immunity"],
                    "rarity": unit["rarity"],
                    "stones": unit["stones"]
                }
            elif target == "skills":
                return_list = {
                    "name": unit["name"],
                    "icon": unit["icon"],
                    "element": unit["element"],
                    "skills": unit["skills"],
                }

    return return_list


def get_stones(stone):
    api = "https://raw.githubusercontent.com/vCel/SS_API/master/stones.json"
    json_obj = requests.get(api)
    data = json_obj.json()

    for thing in data["stones"]:
        if stone in thing["name"].lower():
            return thing

    return "empty"


def get_stonelist():
    api = "https://raw.githubusercontent.com/vCel/SS_API/master/stones.json"
    json_obj = requests.get(api)
    data = json_obj.json()

    stonelist = ""

    for stone in data["stones"]:
        stonelist += "•\t {} [{}]\n".format(stone["name"], stone["element"].capitalize())

    return stonelist
