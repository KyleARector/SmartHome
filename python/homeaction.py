import redis
import json
import requests
import time
import datetime
from zwave import ZStickInterface

db = redis.StrictRedis(host='localhost', port=4747, db=0)

zstick = ZStickInterface()

zwave_sensors = []
wifi_sensors = []

sensors = db.lrange("sensors", 0, -1)
for sensor in sensors:
    sensor = json.loads(sensor)
    if sensor["type"] == "zwave":
        data = {"name": sensor["name"], "node_id": sensor["node_id"], "function": sensor["function"]}
        zwave_sensors.append(data)
    elif sensor["type"] == "wifi":
        data = {"name": sensor["name"], "address": sensor["address"], "function": sensor["function"]}
        wifi_sensors.append(data)

while True:
    size = db.llen("sensor_changes")
    if size > 0:
        for index in range(0, size):
            # Currently only addresses "switch" and "dimmer" function sensors
            try:
                sensor = json.loads(db.lindex("sensor_changes", index))
                db.lrem("sensor_changes", 1, db.lindex("sensor_changes", index))
            except:
                db.lrem("sensor_changes", 1, db.lindex("sensor_changes", index))
                break
            for known_sensor in zwave_sensors:
                if sensor["name"] == known_sensor["name"]:
                    zstick.switch(known_sensor["node_id"], sensor["state"], known_sensor["function"])
                    state = sensor["state"]
                    if state.isdigit():
                        if state > 0:
                            state = "True"
                        else:
                            state = "False"
                    db.set(sensor["name"], state)
                    curr_time = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                    db.lpush(sensor["name"] + " history", str(state) + " - " + curr_time)
                    db.ltrim(sensor["name"] + " history", 0, 99)
                    break
            for known_sensor in wifi_sensors:
                if sensor["name"] == known_sensor["name"]:
                    if sensor["state"] != db.get(sensor["name"]):
                        r = requests.get(known_sensor["address"] + "/relay")
                        db.set(sensor["name"], sensor["state"])
                        curr_time = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                        db.lpush(sensor["name"] + " history", str(sensor["state"]) + " - " + curr_time)
                        db.ltrim(sensor["name"] + " history", 0, 99)
                        break
    for item in zstick.get_sensor_events():
        for known_sensor in zwave_sensors:
            if item["node_id"] == known_sensor["node_id"]:
                db.set(known_sensor["name"], item["state"])
                curr_time = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
                db.lpush(known_sensor["name"] + " history", str(item["state"]) + " - " + curr_time)
                db.ltrim(known_sensor["name"] + " history", 0, 99)
                break


zstick.stop_network()
