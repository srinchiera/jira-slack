from jira_api import JiraApi
import shlex

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

def parse_slack_string(slack_string, username, api):

	try:

		words = shlex.split(slack_string)

		mode = words[0].lower()

		assignee = get_query_arg(words, '-a')
		project = get_query_arg(words, '-p')
		reporter = get_query_arg(words, '-r')
		description = get_query_arg(words, '-d')
		status = get_query_arg(words, '-s')
		issue_type = get_query_arg(words, '-t').lower()

		if issue_type:
			issue_type = issue_type_map[issue_type]

		if mode == 'show':
			project = words[1]
			if not all([project]):
				raise Exception
			else:
				return api.show(project, issue_type=issue_type, assignee=assignee)
		elif mode == 'modify':
			ticket_id = words[1]
			if not all([ticket_id]):
				raise Exception
			else:
				return api.modify(ticket_id, assignee=assignee, reporter=reporter, status=status)
		elif mode == 'create':
			title = words[1]
			if not issue_type:
				issue_type = 'Task'
			if not reporter:
				reporter = username
			if not all([title, project reporter, issue_type]):
				raise Exception
			else:
				return api.create(project, title, issue_type, assignee=assignee, reporter=reporter, description=description)

	except:
		print "Error parsing command, please consult the documentation"
		raise Exception



def get_query_arg(words, flag):

	if flag in words:
		return words[words.index(flag)+1]
	else:
		return None