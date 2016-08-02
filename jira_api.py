from config import (
    JIRA_URL,
    BROWSE_FORMAT_STRING
)
from jira import JIRA
from tabulate import tabulate


class JiraApi(object):
    """Object used to communicate with API"""

    def __init__(self, username, password):
        """Establishes connection to JIRA Api"""

        self.client = JIRA(JIRA_URL, basic_auth=(username, password))
        self.show_headers = ['Link', 'Issue Type', 'Status', 'Assignee']


    def create(self, project, summary, issue_type, reporter, assignee=None,
               description=None):
        """Creates a JIRA issue with parameters. Returns link to ticket."""

        issue_params = {
            'project': {'key': project},
            'summary': summary,
            'issuetype': {'name': issue_type}
        }

        if assignee:
            issue_params['assignee'] = {'name': assignee}

        if reporter:
            issue_params['reporter'] = {'name': reporter}

        if description:
            issue_params['description'] = description

        new_issue = self.client.create_issue(fields=issue_params)
        return BROWSE_FORMAT_STRING.format(new_issue.key)


    def show(self, project, status=None, issue_type=None, assignee=None):
        """Returns all open JIRA issues matching param filters"""

        search_string = 'project={}'.format(project)
        if issue_type:
            search_string += ' and issuetype = {}'.format(issue_type)
        if assignee:
            search_string += ' and assignee = {}'.format(assignee)

        if status:
            search_string += ' and status = {}'.format(status)
        else:
            search_string += ' and resolution = Unresolved'


        issues = self.client.search_issues(search_string)
        issue_values = [self.get_issue_values(issue) for issue in issues]
        return tabulate(issue_values, headers=self.show_headers)


    def modify(self, issue, assignee=None, reporter=None, status=None):
        """Modifies attributes for specified issue key"""

        if status:
            transitions = self.client.transitions(issue)
            transition_id = None
            for transition in transitions:
                transition_name = transition['name'].strip()
                if status == transition_name:
                    transition_id = transition['id']
                    break

            if transition_id is None:
                print "Error!"
                return

            self.client.transition_issue(issue, transition_id)

        issue_params = {}
        if assignee:
            issue_params['assignee'] = {'name': assignee}
        if reporter:
            issue_params['assignee'] = {'name': assignee}

        if issue_params:
            issue = self.client.issue(issue)
            issue.update(fields=issue_params)

        return BROWSE_FORMAT_STRING.format(issue_key.upper())


    def get_issue_values(self, issue):
        """Returns list of issue values for issue object."""

        issue_key = issue.key
        link = BROWSE_FORMAT_STRING.format(issue_key)
        issue_type = issue.raw['fields']['issuetype']['name']
        status = issue.raw['fields']['status']['name']

        try:
            assignee = issue.raw['fields']['assignee']['name']
        except:
            assignee = 'Unassigned'

        return [link, issue_type, status, assignee]
