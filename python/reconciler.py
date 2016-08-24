import time
import json
import requests
import redis
from smartthings import SmartThingsInterface

db = redis.StrictRedis(host='localhost', port=4747, db=0)

infile = open("config.json", "r")
config = json.load(infile)
infile.close()

smartthing = SmartThingsInterface(config["smartthings"])

while True:
    sensor_data = smartthing.get()
    for sensor in sensor_data:
        if sensor["value"] == "on" or sensor["value"] == "active" or sensor["value"] == "open":
            state = "True"
        else:
            state = "False"
        if state != db.get(sensor["name"]):
            db.set(sensor["name"], state)
    time.sleep(1)

