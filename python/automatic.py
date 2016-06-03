import requests
import json
from BeautifulSoup import BeautifulSoup


class AutomaticInterface(object):
    def __init__(self):
        infile = open("mappings.json", "r")
        self.mappings = json.load(infile)
        infile.close()

        infile = open("config.json", "r")
        self.config = json.load(infile)
        infile.close()

    def get_fuel_cost(self, car_name):
        cost = "No cars found with name " + car_name
        car_id = ""
        car_num = 0
        for car in self.mappings["automatic"]["cars"]:
            if car["display_name"] == car_name:
                car_id = car["id"]
                break
            car_num += 1
        if car_id != "":
            headers = {'Authorization': "Bearer " + self.config["automatic"]["access_token"]}
            req = requests.get(self.config["automatic"]["url"] + car_id, headers=headers)
            data = req.json()
            # Check for expired accesss token
            if "error" in data and data["detail"] == "Invalid token":
                self.refresh_access_token()
                headers = {'Authorization': "Bearer " + self.config["automatic"]["access_token"]}
                req = requests.get(self.config["automatic"]["url"] + car_id, headers=headers)
                data = req.json()
            tank_size = (float(self.mappings["automatic"]["cars"][car_num]["tank_size"]))
            gal_of_fuel = (tank_size * float(data["fuel_level_percent"]))/100
	    empty_vol = tank_size - gal_of_fuel
            #req = requests.get("http://fuelgaugereport.aaa.com/import/currentav/display.php?lt=national&ls=US")
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
                'client_id': self.config["automatic"]["client_id"],
                'client_secret': self.config["automatic"]["client_secret"],
                'refresh_token': self.config["automatic"]["refresh_token"]}
        req = requests.post(url, data=data)
        new_token_data = req.json()
        # Write new information to config in case of reboot
        infile = open("config.json", "r")
        data = json.load(infile)
        infile.close()

        data["automatic"]["access_token"] = new_token_data["access_token"]
        data["automatic"]["refresh_token"] = new_token_data["refresh_token"]

        self.config = data

        outfile = open("config.json", "w")
        outfile.write(json.dumps(data))
        outfile.close()
