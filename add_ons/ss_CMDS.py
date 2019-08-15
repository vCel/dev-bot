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
