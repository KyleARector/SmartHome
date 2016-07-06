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
            if str(item["project_id"]) == self.config["project_id"]:
                if str(item["due_date_utc"]) != "None":
                    task_date = item["due_date_utc"]
                    task_date = task_date.replace(" +0000", "")
                    task_datetime = datetime.datetime.strptime(task_date, '%a %d %b %Y %H:%M:%S')
                    task_datetime = task_datetime - datetime.timedelta(hours=6)
                    if datetime.datetime.now().date() == task_datetime.date():
                        return_vals.append(item["content"])
        return return_vals
