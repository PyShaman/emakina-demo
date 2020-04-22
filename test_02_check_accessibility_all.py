import datetime
import unittest
import os
import shutil
from jira import JIRA
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from access.check import AxeEngine
from data.get_data_from_url import get_data_from_xml_sitemap

timestamp = str(datetime.datetime.now().isoformat()).replace(":", "-")[:10]


class TestAccessibilityAllRules(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global driver
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--enable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

    @classmethod
    def tearDownClass(cls):
        driver.quit()
        os.remove(f"a11y_{timestamp}.zip")

    @staticmethod
    def test_01_prepare_directory():
        try:
            os.mkdir(f"results/{timestamp}_all")
            os.mkdir(f"results/{timestamp}_all/flanders_nl")
            os.mkdir(f"results/{timestamp}_all/brussels_fr")
        except OSError:
            print(f"Creation of the directory {timestamp} failed")
        else:
            print(f"Successfully created the directory {timestamp}")

    @staticmethod
    def test_02_all_sites_flanders_nl():
        ae = AxeEngine()
        results = get_data_from_xml_sitemap("https://www.servicevoucher-vl-nl.acc.sodexo.be")
        for result in results:
            site_name = result[47:]
            driver.get(result)
            ae.inject_all_rules(driver, timestamp, "flanders_nl", f"flanders_nl_{site_name}.txt", result)

    @staticmethod
    def test_03_all_sites_brussels_fr():
        ae = AxeEngine()
        results = get_data_from_xml_sitemap("https://www.servicevoucher-bl-fr.acc.sodexo.be")
        for result in results:
            site_name = result[47:]
            driver.get(result)
            ae.inject_all_rules(driver, timestamp, "brussels_fr", f"brussels_fr{site_name}.txt", result)

    @staticmethod
    def test_04_zip_results():
        shutil.make_archive(f"a11y_{timestamp}", "zip", f"results/{timestamp}_all")

    @staticmethod
    def test_05_send_report_to_jira():
        user = "mib@emakina.com"
        apikey = "1D0a0rdqRq5xdAYg9oUH5EF8"
        server = "https://emakina-jira-python-demo.atlassian.net/"
        options = {'server': server}
        jira = JIRA(options, basic_auth=(user, apikey))
        jira.project("EPJD")
        jira.create_issue(project="EPJD",
                          summary=f"Accessibility testing {timestamp}",
                          description="Accessibility testing report",
                          issuetype={"name": "Task"},
                          assignee="mib@emakina.com")
        issues_in_project = jira.search_issues('project=EPJD')
        newest_issue = issues_in_project[0]
        jira.add_attachment(issue=newest_issue, attachment=f"a11y_{timestamp}.zip")


if __name__ == "__main__":
    unittest.main(warnings="ignore")