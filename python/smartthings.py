import requests


class SmartThingsInterface(object):
    def __init__(self, config):
        self.config = config

    def get(self):
        endpt = "/sensors"
        headers = {'Authorization': "Bearer " + self.config["access_token"]}
        req = requests.get(config["url"] + endpt, headers=headers)
        data = req.json()
        return data

    def post(self, device, command):
        endpt = "/sensors"
        headers = {'Authorization': "Bearer " + self.config["access_token"]}
        payload = {"device": device, "command": command}
        req = requests.post(config["url"] + endpt, headers=headers, json=payload)
        data = req.json()
        return data
