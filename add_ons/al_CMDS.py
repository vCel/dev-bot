import requests

def get_ship(name):
    name = name.replace(" ", "%20")  # replaces the blank space with a "-"

    api = "https://azurlane-api.appspot.com/v1/ship?name={}".format(name)
    json_obj = requests.get(api)
    data = json_obj.json()

    return data


def get_rarity(rarity):
    rarity = rarity.replace(" ", "%20")  # replaces the blank space with a "-"

    api = "https://azurlane-api.appspot.com/v1/ships?orderBy=rarity&rarity={}".format(rarity)
    json_obj = requests.get(api)
    data = json_obj.json()

    return data
