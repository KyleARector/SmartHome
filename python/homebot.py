import time
import json
from slackclient import SlackClient
from automatic import AutomaticInterface

infile = open("config.json", "r")
config = json.load(infile)
infile.close()

auto = AutomaticInterface()
sc = SlackClient(config["slack"]["access_token"])

if sc.rtm_connect():
    while True:
        chat = sc.rtm_read()
        for item in chat:
            if "type" in item and item["type"] == "message":
                if "gas" in item["text"] or "fuel" in item["text"]:
                    if "Ford" in item["text"]:
                        cost = auto.get_fuel_cost("Ford")
                        message = "It would cost " + cost + " to fill up right now"
                        sc.rtm_send_message(item["channel"], message)
                    elif "Mazda" in item["text"]:
                        cost = auto.get_fuel_cost("Mazda")
                        message = "It would cost " + cost + " to fill up right now"
                        sc.rtm_send_message(item["channel"], message)
                elif "hey" in item["text"] or "hello" in item["text"]:
                    sc.rtm_send_message(item["channel"], "Hello! How are you?")
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"
