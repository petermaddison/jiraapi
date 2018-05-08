from classes.jira_api import JIRAApi
import requests
import json
import base64
import sys
import getopt
import argparse
from datetime import datetime
from datetime import timedelta

FIRST_STATE = "MSP Sprint 1"
FINAL_STATE = "Done"

def return_issue (issue,fields):
    a=JIRAApi('admin','admin')
    out=a.get_issue(issue,fields)
    return print(out.json())

def return_versions (fixVersion,fields='all'):
    a=JIRAApi('admin','admin')
    out=a.get_issues_in_release(fixVersion,fields)
    return print(out.json())

def return_log (issue):
    a=JIRAApi('admin','admin')
    out=a.get_issue_changelog(issue)
    return print(out.json())

def transition (project,fields='all',first_state=FIRST_STATE, final_state=FINAL_STATE):
    a=JIRAApi('admin','admin')
    get_issues=a.get_issues_in_project(project,fields)
    all_issues=get_issues.json()
    issues = all_issues['issues']
    for issue in issues:
        issue_content = a.get_issue_changelog(issue['key'])
        changelog = issue_content.json()['changelog']
        histories = changelog['histories']
        start_time = datetime.now()-timedelta(days=365*1000) # :-) , sometime back in time
        end_time = datetime.now()-timedelta(days=365*1000)
        quick_transition = True
        g=get_issue_summary(issue['key'])
        for history in histories:
            item = history['items'][0]
            created = history['created']
            if (item['field']=="status" or item['field']=="resolution" or item['field']=="Sprint"):
                if (item['toString']==first_state):
                    timeTransitioned = datetime.strptime((history['created'])[:-9], '%Y-%m-%dT%H:%M:%S') # -9 to trim UTC/mms
                    quick_transition = False
                    if (timeTransitioned>start_time):
                        start_time = timeTransitioned
                elif(item['toString']==final_state):
                    timeTransitioned = datetime.strptime((history['created'])[:-9], '%Y-%m-%dT%H:%M:%S') # -9 to trim UTC/mms
                    if (timeTransitioned>end_time):
                        end_time = timeTransitioned
        if (quick_transition) or (end_time < start_time):
            start_time = end_time
        print(str(issue['key'])+";"+str(g)+";"+str(issue['self'])+";"+str(end_time-start_time))

