from jira import JIRA
from jira_api import JiraApi

from config import (
    JIRA_URL,
    USERNAME,
    PASSWORD,
)

jira_client = JIRA(JIRA_URL, basic_auth=(USERNAME, PASSWORD))
jira_api = JiraApi(jira_client)

'''
jira_api.create(project='OIQ',
                summary='this is a test',
                issue_type='Bug',
                assignee='srinchiera',
                reporter='srinchiera',
                description='wow so cool!')
'''

'''
jira_api.modify('OIQ-683', assignee='jhogan', status='Reopen')
'''

jira_api.show('OIQ-683', assignee='jhogan')

#issue = jira.issue('OIQ-674')
#print issue.fields.project.key             # 'JRA'
#print issue.fields.issuetype.name          # 'New Feature'
#print issue.fields.reporter.displayName    # 'Mike Cannon-Brookes [Atlassian]'
