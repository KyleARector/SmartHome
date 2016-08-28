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
    try:
        sensor_data = smartthing.get("sensors")
    except:
        print "Error getting data"
        sensor_data = []
    for sensor in sensor_data:
        if sensor["value"] == "on" or sensor["value"] == "active" or sensor["value"] == "open" \
                or sensor["value"] == "present":
            state = "True"
        else:
            state = "False"
        if state != db.get(sensor["name"]):
            db.set(sensor["name"], state)
    time.sleep(1)

