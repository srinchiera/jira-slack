import time
from slackclient import SlackClient
from jira import JIRA
from jira_api import JiraApi
import string_parser as parse

from config import (
    JIRA_URL,
    USERNAME,
    PASSWORD,
    TOKEN
)

def start():

    """Start bot"""

    token = TOKEN
    sc = SlackClient(token)
    jira_client = JIRA(JIRA_URL, basic_auth=(USERNAME, PASSWORD))
    jira_api = JiraApi(jira_client)

    if sc.rtm_connect():
        while True:
            events = sc.rtm_read()
            for event in events:
                if event.get("type") == "message":
                    if event.get("text"):
                        user_id = event.get("user")
                        user_name = sc.server.users.find(user_id).name
                        msg = event.get("text")
                        parse.parse_slack_string(msg, user_name, jira_api)

            time.sleep(0.1)
    else:
        print "Connection Failed, invalid token?"
