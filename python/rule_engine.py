import json
import redis

db = redis.StrictRedis(host='localhost', port=4747, db=0)

sensors_list = []

sensors = db.lrange("sensors", 0, -1)
for sensor in sensors:
    sensor = json.loads(sensor)
    sensors_list.append(sensor["name"])

while True:
    sensor_states = []
    for sensor in sensors_list:
        state = db.get(sensor)
        sensor_states.append({"name": sensor, "state": state})
