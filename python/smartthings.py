import requests


class SmartThingsInterface(object):
    def __init__(self, config):
        self.config = config

    def get(self):
        endpt = "/sensors"
        headers = {'Authorization': "Bearer " + self.config["access_token"]}
        req = requests.get(self.config["url"] + endpt, headers=headers)
        data = req.json()
        return data

    def post(self, endpt, device, state):
        endpt = "/" + endpt
        if state == "False":
            command = "off"
        else:
            command = "on"
        headers = {'Authorization': "Bearer " + self.config["access_token"]}
        payload = {"device": device, "command": command}
        req = requests.post(self.config["url"] + endpt, headers=headers, json=payload)
