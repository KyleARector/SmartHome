import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time


class ZStickInterface(object):
    def __init__(self):
        self.device = "/dev/ttyACM0"
        # If using older Z-sticks, use the below device:
        # self.device = "/dev/ttyUSB0"
        # Change config paths where appropriate
        self.options = ZWaveOption(self.device, config_path="/home/pi/Dev/plugins/python-openzwave/openzwave/config",
                                   user_path="/home/pi/Dev/plugins/python-openzwave/config", cmd_line="")
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

    def get_node_by_name(self, name):
        node_id = 0
        for node in self.network.nodes:
            if node.name == name:
                node_id = node.node_id
        return node_id

    def stop_network(self):
        self.network.stop()


def main():
    zstick = ZStickInterface()
    while True:
        node_id = raw_input("Enter a node id: ")
        zstick.toggle_switch(int(node_id))
    zstick.stop_network()

if __name__ == '__main__':
    main()
