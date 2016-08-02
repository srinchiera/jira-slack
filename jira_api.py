from jira import JIRA

def create(jira, project, assignee, reporter, title, description):
    """Creates a JIRA issue with parameters"""

    new_issue = jira.create_issue(project='PROJ_key_or_id',
                                  summary='New issue from jira-python',
                                  description='Look into this one',
                                  issuetype={'name': 'Bug'})
    pass


def show(jira, project, issue_type, username):
    """Returns all open JIRA issues for issue_type and username"""
    pass


def modify(jira, issue, reporter, status):
    """Closes JIRA issue"""
    pass
