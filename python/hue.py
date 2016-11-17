import requests


class HueInterface(object):
    def __init__(self, username, address):
        # Load Hue username on instantiation
        self.username = username
        self.endpt = address + "/api/"

    # Discover new Hue bulbs and return list of ID, name, and type
    # Static method? Return list of addresses?
    # Discover Hue bridges on instantiation of class?
    def discover(self):
        hue_bulbs = []
        req = requests.get(self.endpt + self.username + "/lights")
        response = req.json()
        for item in response.keys():
            data = "{\"name\": \"" + response[item]["name"] + \
                   "\", \"type\": \"hue\", \"function\": \"switch\", " + \
                   "\"id\": " + item + "}"
            hue_bulbs.append(data)
        return hue_bulbs

    # Convert hex color codes to hue/saturation value
    def hex_to_hue_sat(self, hex):
        hue_spec = {"hue": 0, "sat": 0}
        return hue_spec

    # Sets color state of lights.
    # Will probably combine with on/off method
    def set_light_color(self, color, id):
        # Color sent as hex from web interface?
        return True

    # Send on/off command to specific light
    def light_on_off(self, id, state):
        # If the state is true, the value to be set is true
        if state:
            value = "true"
        else:
            value = "false"

        # Create payload to send to bridge
        data = {"on": value}

        # Send the request to the Hue bridge
        req = requests.put(self.endpt + self.username + "/" + "lights/" +
                           str(id), json=data)


def main():
    # Prompt user to press button on Hue Bridge
    input = raw_input("Hit the button on the Hue Bridge, and press Enter.")

    # Perform POST request to retrieve username
    # username = result of post
    username = "newdeveloper"
    address = "127.0.0.1"

    # Instantiate class
    hue = HueInterface(username, address)

if __name__ == "__main__":
    main()