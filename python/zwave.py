import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time
import redis
import json


class ZStickInterface(object):
    def __init__(self):
        self.sensor_list = []
        self.device = "/dev/ttyACM0"
        # If using older Z-sticks, use the below device:
        # self.device = "/dev/ttyUSB0"
        # Change config paths where appropriate
        self.options = ZWaveOption(self.device, config_path="plugins/python-openzwave/openzwave/config",
                                   user_path="plugins/python-openzwave/config", cmd_line="")
        # Turn off ozw console output
        self.options.set_console_output(False)
        self.options.set_save_log_level("Info")
        self.options.set_logging(False)
        self.options.lock()

        print("Starting Network...")
        self.network = ZWaveNetwork(self.options, log=None)
        # Wait for network to start
        while not self.network.state >= self.network.STATE_AWAKED:
            time.sleep(1)
        print("Network Started")

    def toggle_switch(self, node_id):
        try:
            in_work_node = self.network.nodes[node_id]
            switch_val = in_work_node.get_switches().keys()[0]
            if in_work_node.get_switch_state(switch_val):
                in_work_node.set_switch(switch_val, False)
            else:
                in_work_node.set_switch(switch_val, True)
        except:
            print("Invalid node id")

    def switch(self, node_id, state):
        try:
            in_work_node = self.network.nodes[node_id]
            switch_val = in_work_node.get_switches().keys()[0]
            if state == "False":
                in_work_node.set_switch(switch_val, False)
            else:
                in_work_node.set_switch(switch_val, True)
        except:
            print("Invalid node id")

    def stop_network(self):
        self.network.stop()


def main():
    zstick = ZStickInterface()
    db = redis.StrictRedis(host='localhost', port=4747, db=0)

    size = db.llen("sensors")
    for index in range(0, size):
        sensor = json.loads(db.lindex("sensors", index))
        if sensor["type"] == "zwave":
            data = {"name": sensor["name"], "node_id": sensor["node_id"]}
            zstick.sensor_list.append(data)

    while True:
        size = db.llen("sensor_changes")
        if size > 0:
            for index in range(0, size):
                sensor = json.loads(db.lindex("sensor_changes", index))
                for known_sensor in zstick.sensor_list:
                    if sensor["name"] == known_sensor["name"]:
                        db.lrem("sensor_changes", 1, db.lindex("sensor_changes", index))
                        zstick.switch(known_sensor["node_id"], sensor["state"])
                        db.set(sensor["name"], sensor["state"])
                        break

    zstick.stop_network()

if __name__ == '__main__':
    main()
