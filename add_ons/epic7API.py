import requests

def get_latest():
    api = "https://epicsevendb-apiserver.herokuapp.com/api/latest"  # gets the API
    json_obj = requests.get(api)
    data = json_obj.json()

    return data


def get_info(name, etype):
    name = name.replace(" ", "-")  # replaces the blank space with a "-"

    api = "https://epicsevendb-apiserver.herokuapp.com/api/{}/{}".format(etype, name)  # gets the API
    json_obj = requests.get(api)
    data = json_obj.json()

    return data

