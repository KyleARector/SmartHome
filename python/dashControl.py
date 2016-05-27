import requests
import json
import sys 

mac = sys.argv[1] 

with open(config.json) as infile:
    data = json.load(infile) 
infile.close()

root_uri = data["root_uri"]
auth_token = data["auth_token"] 
headers = {"Authorization": "Bearer " + auth_token}

if mac == "my:ma:ca:dd:re:ss": 
    payload = {"button": "2"} 
    req = requests.post(root_uri + "/control", headers=headers, json=payload)
elif mac == "ur:ma:ca:dd:re:ss": 
    payload = {"button": "1"} 
    req = requests.post(root_uri + "/control", headers=headers, json=payload)