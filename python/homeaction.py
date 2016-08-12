import redis
import json
import requests
from zwave import ZStickInterface

zstick = ZStickInterface()
db = redis.StrictRedis(host='localhost', port=4747, db=0)

zwave_sensors = []
wifi_sensors = []

sensors =  db.lrange("sensors", 0, -1)
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
            # Currently only addresses "switch" function sensors
            sensor = json.loads(db.lindex("sensor_changes", index))
            for known_sensor in zwave_sensors:
                if sensor["name"] == known_sensor["name"]:
                    db.lrem("sensor_changes", 1, db.lindex("sensor_changes", index))
                    zstick.switch(known_sensor["node_id"], sensor["state"], known_sensor["function"])
                    db.set(sensor["name"], sensor["state"])
                    break
            for known_sensor in wifi_sensors:
                if sensor["name"] == known_sensor["name"]:
                    db.lrem("sensor_changes", 1, db.lindex("sensor_changes", index))
                    r = requests.get(known_sensor["address"] + "/relay")
                    db.set(sensor["name"], sensor["state"])
                    break

zstick.stop_network()
