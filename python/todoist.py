import requests
import datetime


class TodoistInterface(object):
    def __init__(self, config):
        self.config = config

    def get_today_tasks(self):
        return_vals = []
        data = {'token': self.config["access_token"],
                'sync_token': '*',
                'resource_types': '["items"]'}
        req = requests.get("https://todoist.com/API/v7/sync", data=data)
        data = req.json()
        for item in data["items"]:
            if item["project_id"] == self.config["project_id"]:
                if str(item["due_date_utc"]) != "None":
                    test_date = item["due_date_utc"]
                    test_date = test_date.replace(" +0000", "")
                    date_object = datetime.datetime.strptime(test_date, '%a %d %b %Y %H:%M:%S')
                    date_object = date_object - datetime.timedelta(hours=6)
                    if datetime.datetime.now().date() == date_object.date():
                        return_vals.append(item["content"])
        return return_vals
