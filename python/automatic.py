import requests
import json
from BeautifulSoup import BeautifulSoup


class AutomaticInterface(object):
    def __init__(self, config):
        self.config = config

    def get_fuel_cost(self, car_name):
        cost = "No cars found with name " + car_name
        car_id = ""
        car_num = 0
        for car in self.config["cars"]:
            if car["display_name"] == car_name:
                car_id = car["id"]
                break
            car_num += 1
        if car_id != "":
            headers = {'Authorization': "Bearer " + self.config["access_token"]}
            req = requests.get(self.config["url"] + car_id, headers=headers)
            data = req.json()
            # Check for expired accesss token
            if "error" in data and data["detail"] == "Invalid token":
                self.refresh_access_token()
                headers = {'Authorization': "Bearer " + self.config["access_token"]}
                req = requests.get(self.config["url"] + car_id, headers=headers)
                data = req.json()
            tank_size = (float(self.config["cars"][car_num]["tank_size"]))
            gal_of_fuel = (tank_size * float(data["fuel_level_percent"]))/100
            empty_vol = tank_size - gal_of_fuel
            req = requests.get("http://www.fueleconomy.gov/ws/rest/fuelprices")
            # Need error checking
            parsed = BeautifulSoup(req.text)
            price = parsed.find("regular").text
            price = float(price.replace("$", ""))
            cost = "$" + str(round(price * empty_vol, 2))
        return cost

    def refresh_access_token(self):
        url = "https://accounts.automatic.com/oauth/access_token/"
        data = {'grant_type': 'refresh_token',
                'client_id': self.config["client_id"],
                'client_secret': self.config["client_secret"],
                'refresh_token': self.config["refresh_token"]}
        req = requests.post(url, data=data)
        new_token_data = req.json()
        # Write new information to config in case of reboot
        infile = open("config.json", "r")
        data = json.load(infile)
        infile.close()

        data["automatic"]["access_token"] = new_token_data["access_token"]
        data["automatic"]["refresh_token"] = new_token_data["refresh_token"]

        self.config = data["automatic"]

        outfile = open("config.json", "w")
        outfile.write(json.dumps(data))
        outfile.close()


def main():
    infile = open("config.json", "r")
    config = json.load(infile)
    infile.close()

    config = config["automatic"]

    test = AutomaticInterface(config)
    car = raw_input("Try a vehicle: ")
    out = test.get_fuel_cost(car)
    print out

if __name__ == '__main__':
    main()
