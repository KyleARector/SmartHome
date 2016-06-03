import time
import json
from slackclient import SlackClient
from automatic import AutomaticInterface
from smartthings import SmartThingsInterface
# from langinterface import LanguageInterface

infile = open("config.json", "r")
config = json.load(infile)
infile.close()

slack = SlackClient(config["slack"]["access_token"])
auto = AutomaticInterface(config["automatic"])
smartthing = SmartThingsInterface(config["smartthings"])

if slack.rtm_connect():
    while True:
        chat = slack.rtm_read()
        for item in chat:
            if "type" in item and item["type"] == "message":
                if "gas" in item["text"] or "fuel" in item["text"]:
                    if "Ford" in item["text"]:
                        cost = auto.get_fuel_cost("Ford")
                        message = "It would cost " + cost + " to fill up right now"
                        slack.rtm_send_message(item["channel"], message)
                    elif "Mazda" in item["text"]:
                        cost = auto.get_fuel_cost("Mazda")
                        message = "It would cost " + cost + " to fill up right now"
                        slack.rtm_send_message(item["channel"], message)
                elif "hey" in item["text"] or "hello" in item["text"]:
                    slack.rtm_send_message(item["channel"], "Hello! How are you?")
                elif "home" in item["text"] and "status" in item["text"]:
                    sensor_data = smartthing.get()
                    message = ""
                    for sensor in sensor_data:
                        message += sensor["name"] + " is " + sensor["value"] + "\n"
                    slack.rtm_send_message(item["channel"], message)
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"
