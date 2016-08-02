import shlex
import argparse

issue_type_map = {
    'task': 'Task',
    'bug': 'Bug',
    'new_feature': 'New Feature',
    'improvement': 'Improvement',
    'question': 'Question',
    'story': 'Story',
    'epic': 'Epic',
    'target_result': 'Target Result'
}

slack_parser = argparse.ArgumentParser(description='Interpret slack input to Jira API', add_help=False)
slack_parser.add_argument('-a', action='store', help='Assignee', dest='assignee')
slack_parser.add_argument('-p', action='store', help='Project', dest='project')
slack_parser.add_argument('-r', action='store', help='Reporter', dest='reporter')
slack_parser.add_argument('-d', action='store', help='Description', dest='description')
slack_parser.add_argument('-s', action='store', help='Status', dest='status',
    type=str.lower)
slack_parser.add_argument('-t', action='store', help='Issue Type', dest='issue_type',
    type=str.lower, choices=['task', 'bug', 'new_feature', 'improvement', 'question', 'story',
     'epic', 'target_result'])

create_parser = argparse.ArgumentParser(description='For creating Jira Issues', parents=[slack_parser])
create_parser.add_argument('title', action='store', help='Summary of Jira issue')

modify_parser = argparse.ArgumentParser(description='For modifying Jira Issues', parents=[slack_parser])
modify_parser.add_argument('ticket_id', action='store', help='ID of jira issue, ie ABC-123')

show_parser = argparse.ArgumentParser(description='For showing Jira Issues in a certain project', 
    parents=[slack_parser])
show_parser.add_argument('project', action='store', help='project abbreviation')

def parse_slack_string(command, slack_string, username, api):
    """
    When someone types '/jira blah blah blah' into slack, 'blah blah blah',
    their username, and an instance of the JiraApi are passed into this method,
    which interprets the string and calls the appropriate method in JiraApi
    """

    words = shlex.split(slack_string)

    if command = 'show':
        parser = show_parser
    elif command = 'modify':
        parser = modify_parser
    elif command = 'create':
        parser = create_parser

    try:
        arg_dict = vars(parser.parse_args(words))
    except:
        return parser.parse_args(['-h'])

    assignee = arg_dict['assignee']
    project = arg_dict['project']
    reporter = arg_dict['reporter']
    description = arg_dict['description']
    status = arg_dict['status']
    issue_type = arg_dict['issue_type']
    if issue_type:
        issue_type = issue_type_map[issue_type]

    if command == 'show':
        project = arg_dict['project']
        if not all([project]):
            raise Exception
        else:
            return api.show(project, issue_type=issue_type, assignee=assignee)
    elif command == 'modify':
        ticket_id = arg_dict['ticket_id']
        if not all([ticket_id]):
            raise Exception
        else:
            return api.modify(ticket_id, assignee=assignee, reporter=reporter, status=status)
    elif command == 'create':
        title = arg_dict['title']
        if not issue_type:
            issue_type = 'Task'
        if not reporter:
            reporter = username
        if not all([title, project, reporter, issue_type]):
            raise Exception
        else:
            return api.create(project, title, issue_type, assignee=assignee, 
                reporter=reporter, description=description)

