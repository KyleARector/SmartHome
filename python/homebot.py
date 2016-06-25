import time
import json
import requests
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

sphereAddr = compAddr = tempAddr = "http://localhost"

for item in config["local"]["sensors"]:
    if item["sensor_name"] == "sphere":
        sphereAddr = item["address"]
    elif item["sensor_name"] == "comp_relay":
        compAddr = item["address"]
    elif item["sensor_name"] == "temp_sensor":
        tempAddr = item["address"]

if slack.rtm_connect():
    while True:
        chat = slack.rtm_read()
        for item in chat:
            if "type" in item and item["type"] == "message":
                if "gas" in item["text"].lower() or "fuel" in item["text"].lower():
                    if "ford" in item["text"].lower():
                        auto_data = auto.get_fuel_cost("Ford")
                        message = "It would cost " + str(auto_data["cost"]) + " to fill up " + \
                                  str(auto_data["empty_vol"]) + " gallons"
                        slack.rtm_send_message(item["channel"], message)
                    elif "mazda" in item["text"].lower():
                        auto_data = auto.get_fuel_cost("Mazda")
                        message = "It would cost " + str(auto_data["cost"]) + " to fill up " + \
                                  str(auto_data["empty_vol"]) + " gallons"
                        slack.rtm_send_message(item["channel"], message)
                elif "hey" in item["text"].lower() or "hello" in item["text"].lower():
                    slack.rtm_send_message(item["channel"], "Hello! How are you?")
                elif "home" in item["text"].lower() and "status" in item["text"].lower():
                    sensor_data = smartthing.get()
                    message = ""
                    for sensor in sensor_data:
                        message += sensor["name"] + " is " + sensor["value"] + "\n"
                    slack.rtm_send_message(item["channel"], message)
                elif "plex" in item["text"].lower() or "computer" in item["text"].lower():
                    if "on" in item["text"].lower():
                        command = "on"
                    else:
                        command = "off"
                    slack.rtm_send_message(item["channel"], "The computer is turning " + command)
                    r = requests.get(compAddr + "/relay")
                elif "sphere" in item["text"].lower():
                    r = {}
                    if "red" in item["text"].lower():
                        r = requests.get(sphereAddr + ":8080/sphere?color=red")
                    elif "blue" in item["text"].lower():
                        r = requests.get(sphereAddr + ":8080/sphere?color=blue")
                    elif "green" in item["text"].lower():
                        r = requests.get(sphereAddr + ":8080/sphere?color=green")
                    elif "magenta" in item["text"].lower():
                        r = requests.get(sphereAddr + ":8080/sphere?color=magenta")
                    elif "cyan" in item["text"].lower():
                        r = requests.get(sphereAddr + ":8080/sphere?color=cyan")
                    elif "yellow" in item["text"].lower():
                        r = requests.get(sphereAddr + ":8080/sphere?color=yellow")
                    elif "white" in item["text"].lower():
                        r = requests.get(sphereAddr + ":8080/sphere?color=white") 
                    data = r.json()
                    slack.rtm_send_message(item["channel"], "Turning the sphere " + data["status"])
                elif "temperature" in item["text"].lower() or "temp" in item["text"].lower():
                    r = requests.get(tempAddr)
                    data = r.json()
                    message = "It is " + str(data["variables"]["inTempInt"]) + " degrees inside,and " + \
                              str(data["variables"]["outTempInt"]) + " degrees outside"
                    slack.rtm_send_message(item["channel"], message)
        time.sleep(1)
else:
    print "Connection Failed, invalid token?"
