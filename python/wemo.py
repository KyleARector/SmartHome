import requests


class WeMoInterface(object):
    def __init__(self, config):
        self.headers = {"content-type": "text/xml; charset=utf-8",
                        "SOAPACTION": "\"urn:Belkin:service:basicevent:1#GetBinaryState\"",
                        "accept": ""}

    def send_command(self, address, command):
        if command.lower() == "on":
            binary_command = 1
        else:
            binary_command = 0

        address += "/upnp/control/basicevent1"

        body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + \
               "<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\"" + \
               "\s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\">" + \
               "<s:Body>" + \
               "<u:GetBinaryState xmlns:u=\"urn:Belkin:service:basicevent:1\">" + \
               "<BinaryState>" + binary_command + "</BinaryState>" + \
               "</u:GetBinaryState>" + \
               "</s:Body>" + \
               "</s:Envelope>"

        req = requests.post(url, data=body, headers=self.headers)
        data = req.content
        return data
