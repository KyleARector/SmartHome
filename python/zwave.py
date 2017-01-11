import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import libopenzwave
import time
import json
from sensor import Sensor


class ZStickInterface(object):
    def __init__(self):
        self.sensor_events = []
        self.device = "/dev/ttyACM0"
        config_path = "plugins/python-openzwave/openzwave/config"
        user_path = "plugins/python-openzwave/config"
        # If using older Z-sticks, use the below device:
        # self.device = "/dev/ttyUSB0"
        # Change config paths where appropriate
        self.options = ZWaveOption(self.device, config_path=config_path,
                                   user_path=user_path, cmd_line="")
        # Turn off ozw console output
        self.options.set_console_output(False)
        self.options.set_save_log_level("Info")
        self.options.set_logging(False)
        self.options.lock()

        self.manager = libopenzwave.PyManager()
        self.manager.create()
        self.manager.addWatcher(self.event_callback)
        self.manager.addDriver(self.device)

        print("Starting Z-Wave Network...")
        self.network = ZWaveNetwork(self.options, log=None)
        # Wait for network to start
        while not self.network.state >= self.network.STATE_AWAKED:
            time.sleep(1)
        print("Z-Wave Network Started")

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

    def switch(self, node_id, state, function):
        try:
            in_work_node = self.network.nodes[node_id]
            if function == "dimmer":
                switch_val = in_work_node.get_dimmers().keys()[0]
                if state == "False":
                    in_work_node.set_dimmer(switch_val, 0)
                elif state == "True":
                    in_work_node.set_dimmer(switch_val, 99)
                else:
                    in_work_node.set_dimmer(switch_val, int(state))
            elif function == "switch":
                switch_val = in_work_node.get_switches().keys()[0]
                if state == "False":
                    in_work_node.set_switch(switch_val, False)
                else:
                    in_work_node.set_switch(switch_val, True)
        except:
            print("Invalid node id")

    def event_callback(self, args):
        if args["notificationType"] in ("ValueAdded", "ValueChanged"):
            cmd_class = args["valueId"]["commandClass"]
            if cmd_class == "COMMAND_CLASS_SENSOR_BINARY":
                node_id = args["valueId"]["nodeId"]
                state = args["valueId"]["value"]
                data = {"node_id": node_id, "state": state}
                self.sensor_events.append(data)

    def get_sensor_events(self):
        last_events = self.sensor_events
        self.sensor_events = []
        return last_events

    def stop_network(self):
        self.network.stop()


class ZWaveSensor(Sensor):
    def __init__(self):
        pass


def main():
    zstick = ZStickInterface()
    zstick.stop_network()

if __name__ == '__main__':
    main()
