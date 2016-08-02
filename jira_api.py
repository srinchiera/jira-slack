from jira import JIRA

class JiraApi(object):

    def __init__(self, client):
        self.client = client


    def create(self, project, summary, issue_type,
               assignee=None, reporter=None, description=None):
        """Creates a JIRA issue with parameters"""

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


    def show(self, project, issue_type=None, assignee=None):
        """Returns all open JIRA issues for issue_type and username"""
        project = self.client.project('OIQ')
        print project.__dict__
        jira.search_issues('project=PROJ')


    def modify(self, issue, assignee=None, reporter=None, status=None):
        """Closes JIRA issue"""

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
