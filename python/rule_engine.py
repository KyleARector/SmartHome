import json
import redis


# Holds a collection of rules
# Subscribes to sensor changes and tasks Rule object with evaluation
class RuleEngine(object):
    def __init__(self):
        self.db = redis.StrictRedis(host='localhost', port=4747, db=0)
        self.sensors_list = self.load_sensors()
        self.rules = []

    # Load the sensors from the database
    def load_sensors(self):
        sensor_list = []
        sensors = self.db.lrange("sensors", 0, -1)
        for sensor in sensors:
            sensor = json.loads(sensor)
            sensors_list.append(sensor["name"])
        return sensors_list

    # Get the current state of each sensor from the database
    def get_sensor_states(self):
        sensor_states = []
        for sensor in sensors_list:
            state = db.get(sensor)
            sensor_states.append({"name": sensor, "state": state})
        return sensor_states


# Holds a single rule
# Is collected in RuleEngine and evaluated if criteria met
class Rule(object):
    def __init__(self):
        self.rule = ""
