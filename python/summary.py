import requests
import json
import redis
from todoist import TodoistInterface

db = redis.StrictRedis(host='localhost', port=4747, db=0)

infile = open("/home/pi/Dev/config.json", "r")
config = json.load(infile)
infile.close()

db.rpush("notifications", "Good morning!\n")

# Get inspirational quote
req = requests.get("http://quotes.rest/qod.json?category=life")
data = req.json()
quote = data["contents"]["quotes"][0]["quote"]
author = data["contents"]["quotes"][0]["author"]
db.rpush("notifications", "Here is a quote to start your day:")
db.rpush("notifications", "\"" + quote + "\"")
db.rpush("notifications", " - " + author + "\n")

# Get Tasks
todo = TodoistInterface(config["todoist"])
task_list = todo.get_today_tasks()
task_count = len(task_list)
if task_count != 0:
    task_qty_word = "task"
    if task_count > 1:
        task_qty_word += "s"
    db.rpush("notifications", "You have " + str(task_count) + " " + task_qty_word + " on your to do list today:")
    for item in task_list:
        db.rpush("notifications", " - " + item)
else:
    db.rpush("notifications", "There are no tasks on your to do list today")

