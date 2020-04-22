import time
import unittest
import security.zap as security
import os
from datetime import datetime
from jira import JIRA
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

timestamp = str(datetime.now().isoformat()).replace(":", "-")[:-7]


class TestVulnerabilities(unittest.TestCase):
    zap = security.Zap()
    zap.start_zap()
    print("Checking connection to localhost")
    zap.check_zap_connection()
    print("connected to localhost")
    zap.start_passive_scan()

    @classmethod
    def setUpClass(cls):
        global driver
        proxy_host = "127.0.0.1"
        proxy_port = 8096
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument(f"--proxy-server={proxy_host}:{proxy_port}")
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        zap = security.Zap()
        driver.quit()
        zap.stop_zap()
        os.remove(f"flanders_nl_main_{timestamp}.html")
        os.remove(f"brussels_fr_main_{timestamp}.html")

    @staticmethod
    def test_01_flanders_nl_main_site_for_vulnerabilities():
        zap = security.Zap()
        zap.run_spider("https://www.servicevoucher-vl-nl.acc.sodexo.be", timestamp, "flanders_nl_main_")

    @staticmethod
    def test_02_brussels_fr_main_site_for_vulnerabilities():
        zap = security.Zap()
        zap.run_spider("https://www.servicevoucher-bl-fr.acc.sodexo.be", timestamp, "brussels_fr_main_")

    @staticmethod
    def test_03_send_report_to_jira():
        user = "mib@emakina.com"
        apikey = "1D0a0rdqRq5xdAYg9oUH5EF8"
        server = "https://emakina-jira-python-demo.atlassian.net/"
        options = {'server': server}
        jira = JIRA(options, basic_auth=(user, apikey))
        jira.project("EPJD")
        jira.create_issue(project="EPJD",
                          summary=f"Vulnerability testing {timestamp}",
                          description="Vulnerability testing report",
                          issuetype={"name": "Task"},
                          assignee="mib@emakina.com")
        issues_in_project = jira.search_issues('project=EPJD')
        newest_issue = issues_in_project[0]
        jira.add_attachment(issue=newest_issue, attachment=f"flanders_nl_main_{timestamp}.html")
        jira.add_attachment(issue=newest_issue, attachment=f"brussels_fr_main_{timestamp}.html")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
