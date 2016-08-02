from jira import JIRA

from config import (
    JIRA_URL,
    USERNAME,
    PASSWORD,
)

jira = JIRA(JIRA_URL, basic_auth=(USERNAME, PASSWORD))

issue = jira.issue('OIQ-674')
print issue.fields.project.key             # 'JRA'
print issue.fields.issuetype.name          # 'New Feature'
print issue.fields.reporter.displayName    # 'Mike Cannon-Brookes [Atlassian]'
