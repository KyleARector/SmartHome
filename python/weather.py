import requests
import time
import redis

db = redis.StrictRedis(host='localhost', port=4747, db=0)

base_url = "https://api.darksky.net/forecast/key_long_lat"

sphereAddr = "ad.dr.e.ss"

data = requests.get(base_url)

spec_data = data.json()
weather_data = spec_data["currently"]["summary"]
outside_temp = spec_data["currently"]["temperature"]
apparent_temp = spec_data["currently"]["apparentTemperature"]
sunrise = spec_data["daily"]["data"][0]["sunriseTime"]
sunset = spec_data["daily"]["data"][0]["sunsetTime"]
now = time.time()

db.set("weatherTemp", outside_temp)
db.set("weatherFeelTemp", apparent_temp)
db.set("weatherConditions", weather_data)

if weather_data == "Heavy Rain":
    # Color: Blue
    r = requests.get(sphereAddr + ":8080/sphere?color=blue")
elif weather_data == "Light Rain" or spec_data == "Drizzle":
    # Color: Cyan
    r = requests.get(sphereAddr + ":8080/sphere?color=cyan")
elif weather_data == "Overcast" or "Cloudy" in spec_data:
    # Color: Magenta
    r = requests.get(sphereAddr + ":8080/sphere?color=magenta")
elif weather_data == "Clear" or "Sunny" in spec_data:
    # Color: Yellow or White
    if now < sunrise or now > sunset:
        # Night
        r = requests.get(sphereAddr + ":8080/sphere?color=white")
    else:
        # Day
        r = requests.get(sphereAddr + ":8080/sphere?color=yellow")
