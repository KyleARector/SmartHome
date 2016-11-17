import redis
import json
import requests
import time
import datetime
from zwave import ZStickInterface
from hue import HueInterface

# Set up database connection
db = redis.StrictRedis(host='localhost', port=4747, db=0)

# Initialize Z-wave network
zstick = ZStickInterface()

# Instantiate Hue Light helper
hue = HueInterface(db.get("hue_username"), db.get("hue_address"))
# Need to check if sensors already exist in database
# Remove items that are in db but not in recent discovery
'''hue_data = hue.discover()
for item in data:
    db.rpush("sensors", item)'''

# Initialize sensor lists
zwave_sensors = []
wifi_sensors = []
hue_sensors = []

# Query database for sensors and sort into lists by type
sensors = db.lrange("sensors", 0, -1)
for sensor in sensors:
    sensor = json.loads(sensor)
    if sensor["type"] == "zwave":
        data = {"name": sensor["name"], "node_id": sensor["node_id"],
                "function": sensor["function"]}
        zwave_sensors.append(data)
    elif sensor["type"] == "wifi":
        data = {"name": sensor["name"], "address": sensor["address"],
                "function": sensor["function"]}
        wifi_sensors.append(data)
    elif sensor["type"] == "hue":
        data = {"name": sensor["name"], "id": sensor["id"],
                "function": sensor["function"]}
        hue_sensors.append(data)


# Get current time and push to database for history
# Arguments are the sensor's name and the state to write to history
def log_sensor_history(sensor_name, sensor_state):
    curr_time = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")
    if (db.get(sensor_name) != sensor_state):
        db.lpush(sensor_name + " history", sensor_state + " - " +
                 curr_time)
        db.ltrim(sensor_name + " history", 0, 149)

# Query database for sensor Changes
# Loop constantly
while True:
    # Check size of sensor changes lists
    # If 0, do nothing
    size = db.llen("sensor_changes")
    if size > 0:
        # Loop through queried sensor changes
        for index in range(0, size):
            # Try parsing the JSON record of sensor change
            # If successful, continue, if not remove the item from the list
            # Currently only addresses "switch" and "dimmer" function sensors
            try:
                sensor = json.loads(db.lindex("sensor_changes", index))
                db.lrem("sensor_changes", 1,
                        db.lindex("sensor_changes", index))
            except:
                db.lrem("sensor_changes", 1,
                        db.lindex("sensor_changes", index))
                break
            # Check sensor against known Z-wave sensors
            for known_sensor in zwave_sensors:
                if sensor["name"] == known_sensor["name"]:
                    # Set the switch/dimmer to the requested state
                    zstick.switch(known_sensor["node_id"], sensor["state"],
                                  known_sensor["function"])
                    state = sensor["state"]
                    # If dimmer value set, correlate value to on/off state
                    # 0 is off, anything above is on
                    if state.isdigit():
                        if state > 0:
                            state = "True"
                        else:
                            state = "False"
                    # Record the state in the database
                    db.set(sensor["name"], state)
                    log_sensor_history(sensor["name"], str(state))
                    break
            # Check sensor against known wifi sensors
            # Currently supports on/off relays
            for known_sensor in wifi_sensors:
                if sensor["name"] == known_sensor["name"]:
                    if sensor["state"] != db.get(sensor["name"]):
                        # Try to send an HTTP request to the device
                        # Only set state if request is successful
                        # Should add verification from Arduino response
                        try:
                            r = requests.get(known_sensor["address"] +
                                             "/relay")
                            # Record the state in the database
                            db.set(sensor["name"], sensor["state"])
                            log_sensor_history(sensor["name"],
                                               str(sensor["state"]))
                        except:
                            pass
                        break
            # Check against known Hue bulbs
            # Currently supports on/off of lights
            # Will support color/dimming
            for known_sensor in hue_sensors:
                if sensor["name"] == known_sensor["name"]:
                    hue.light_on_off(known_sensor["id"], sensor["state"])
                    log_sensor_history(known_sensor["name"],
                                       str(sensor["state"]))
                    break
    # Query Z-wave interface for non-interactive sensor changes
    # This includes changes from contact and motion sensors
    # Needs to support power level, etc
    # Currently supports only Z-wave, only checks against known Z-wave sensors
    for item in zstick.get_sensor_events():
        for known_sensor in zwave_sensors:
            if item["node_id"] == known_sensor["node_id"]:
                # Record the state in the database
                db.set(known_sensor["name"], item["state"])
                log_sensor_history(known_sensor["name"], str(item["state"]))
                break

# If loop exits, stop Z-wave network
zstick.stop_network()
