from jira import JIRA
from datetime import datetime

user = 'mib@emakina.com'
apikey = 'F0ub9n6ej8TuK0YoNfqO7B38'
server = 'https://emakina-jira-python-demo.atlassian.net/'

options = {
 'server': server
}
timestamp = str(datetime.now().isoformat()).replace(":", "-")[:19]

jira = JIRA(options, basic_auth=(user, apikey))

project = jira.project("EPJD")
new_issue = jira.create_issue(project="EPJD",
                              summary=f"Accessibility testing {timestamp}",
                              description="Accessibility testing report",
                              issuetype={"name": "Task"})
