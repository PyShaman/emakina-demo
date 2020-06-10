from jira import JIRA


class Jira:

    def __init__(self):
        self.user = "your@email.com"
        self.apikey = "your_jira_api_key"
        self.server = "https://your_emakina_jira_instance.com"
        self.project = "your_project_name"
        self.options = {'server': self.server}
        self.jira = JIRA(self.options, basic_auth=(self.user, self.apikey))

    def create_issue(self, summary, description, timestamp):
        self.jira.project(self.project)
        self.jira.create_issue(project=self.project,
                               summary=f"{summary} {timestamp}",
                               description=f"{description}",
                               issuetype={"name": "Task"})

    def add_attachment_to_ticket(self, filename):
        self.jira.add_attachment(issue=self.jira.search_issues(f'project={self.project}')[0],
                                 attachment=f"{filename}")
