import requests
import datetime


# Create class to interface with Todoist API
class TodoistInterface(object):
    # Load passed in config
    def __init__(self, config):
        self.config = config

    # Get tasks assigned to today
    # Returns list of strings denoting the tasks
    def get_today_tasks(self):
        # Intialize return values
        return_vals = []
        # Create parameters for get request
        data = {'token': self.config["access_token"],
                'sync_token': '*',
                'resource_types': '["items"]'}
        # Request all tasks from Todoist
        req = requests.get("https://todoist.com/API/v7/sync", data=data)
        data = req.json()
        # Determine if task is in allowable projects from config
        for item in data["items"]:
            if str(item["project_id"]) == self.config["project_id"]:
                # Only look at tasks that have assigned dates
                if str(item["due_date_utc"]) != "None":
                    task_date = item["due_date_utc"]
                    # Remove timezone offset
                    task_date = task_date.replace(" +0000", "")
                    # Get current date
                    task_datetime = datetime.datetime.strptime(task_date, '%a %d %b %Y %H:%M:%S')
                    # Translate to current timezone
                    # Needs to be set dynamically
                    task_datetime = task_datetime - datetime.timedelta(hours=6)
                    # If task is due today, append it to the list to return
                    if datetime.datetime.now().date() == task_datetime.date():
                        return_vals.append(item["content"])
        return return_vals
