import requests
from datetime import datetime
import dateutil.parser
from reports.models import *
from api_handler.views import write_into_model
from api_handler.models import *
import django
# def main():
project_path = "/api/v1/data?format=json"
cron_settings = CronSetting.objects.all()[0]
server_url = cron_settings.server_url.strip("/")
auth = (cron_settings.username,cron_settings.password)
projects_response = requests.get(server_url+project_path,auth=auth)
projects = projects_response.json()
last_submission_time = cron_settings.last_submission_time
print(last_submission_time)
new_submission_time = None
flag = False

# print((projects))
for project in projects:
    # print(project)
    # print(project.get("id_string").lower(), cron_settings.project_name.lower())
    if project.get("id_string").lower() == cron_settings.project_name.lower():
        # print (project)
        project_url = project.get("url")
        submissions_response = requests.get(project_url,auth=auth)
        submissions = submissions_response.json()
        for submission in submissions:
            submission_time = dateutil.parser.parse(submission.get("_submission_time")+"+00:00")
            if submission_time > last_submission_time:
                s = {}
                for key in submission.keys():
                    s[key.split("/")[-1]] = submission[key]
                write_into_model(s, dateutil.parser.parse(submission.get("_submission_time")), None, 1)
                if flag:
                    if new_submission_time < submission_time:
                        new_submission_time = submission_time
                        print("goneto 1")
                else:
                    new_submission_time = submission_time
                    flag = True

print("gone 1.5")
if flag:
    print("goneto 2")
    cron_settings.last_submission_time = new_submission_time
    cron_settings.save()
else:
    print("submission time", new_submission_time)

print("ended")
