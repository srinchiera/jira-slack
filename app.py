from jira import JIRA
from jira_api import JiraApi
import bot

from config import (
    JIRA_URL,
    USERNAME,
    PASSWORD,
)

def main():
    bot.start()

if __name__ == '__main__':
    main()


'''
jira_client = JIRA(JIRA_URL, basic_auth=(USERNAME, PASSWORD))
jira_api = JiraApi(jira_client)

jira_api.create(project='OIQ',
                summary='this is a test2',
                issue_type='Bug',
                assignee='jdavison',
                reporter='srinchiera',
                description='wow so cool!')

jira_api.modify('OIQ-683', assignee='jhogan', status='Reopen')

jira_api.show('OIQ', assignee='srinchiera', issue_type='Bug')

'''
