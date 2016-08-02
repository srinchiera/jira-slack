import time
from slackclient import SlackClient
from jira_api import JiraApi
import string_parser as parse

from config import (
    USERNAME,
    PASSWORD,
    TOKEN
)


def start():
    """Start bot"""

    token = TOKEN
    sc = SlackClient(token)
    jira_api = JiraApi(USERNAME, PASSWORD)

    if not sc.rtm_connect():
        raise Exception("Connection Failed, invalid token?")

    while True:
        events = sc.rtm_read()
        for event in events:
            handle_event(sc, event)


def handle_event(sc, event):
    """Processes event message and making call to API when necessary"""

    event_type = event.get("type")
    message = event.get("text", '').split()
    user_id = event.get("user")
    channel = event.get("channel")

    # Disregard unwanted messages
    if (event_type != "message" or
        len(message) < 2 or
        message[0] != '!jira'):
        return

    command = message[1]
    args = message[2:]

    user_id = event.get("user")
    user_name = sc.server.users.find(user_id).name

    response = parse.parse_slack_string(command, args, user_name, jira_api)
    sc.rtm_send_message(channel, response)
