import time
import json
import redis
from hue import HueInterface

db = redis.StrictRedis(host='localhost', port=4747, db=0)

hue = HueInterface(db.get("hue_username"), db.get("hue_address"))

while True:
    try:
        sensor_data = hue.get_lights()
    except:
        print "Error getting data"
        sensor_data = {}
    for item in sensor_data.keys():
        sensor_data[item]["name"]
        if sensor_data[item]["state"]["on"]:
            state = "True"
        else:
            state = "False"
        if state != db.get(sensor_data[item]["name"]):
            db.set(sensor_data[item]["name"], state)
    time.sleep(1)
