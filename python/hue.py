import requests


class HueInterface(object):
    def __init__(self, username):
        # Load Hue username on instantiation
        self.username = username

    # Discover new Hue bulbs and return list of ID, name, and type
    # Static method? Return list of addresses?
    def discover(self):
        hue_bulbs = []
        return hue_bulbs

    # Convert hex color codes to hue/saturation value
    def hex_to_hue_sat(hex):
        hue_spec = {"hue": 0, "sat": 0}
        return hue_spec


def main():
    # Prompt user to press button on Hue Bridge
    input = raw_input("Hit the button on the Hue Bridge, and press Enter.")

    # Perform POST request to retrieve username
    # username = result of post
    username = "newdeveloper"

    # Instantiate class
    hue = HueInterface(username)

if __name__ == "__main__":
    main()
