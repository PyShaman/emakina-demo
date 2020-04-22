import time
import unittest
import security.zap as security
import os
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from data.jira_access import Jira

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
        zap.run_spider("https://www.servicevoucher-vl-nl.acc.sodexo.be", timestamp, "flanders_nl_main")

    @staticmethod
    def test_02_brussels_fr_main_site_for_vulnerabilities():
        zap = security.Zap()
        zap.run_spider("https://www.servicevoucher-bl-fr.acc.sodexo.be", timestamp, "brussels_fr_main")

    @staticmethod
    def test_03_send_report_to_jira():
        jira = Jira()
        jira.create_issue("Vulnerability testing", "Vulnerability testing report", timestamp)
        jira.add_attachment_to_ticket(f"flanders_nl_main_{timestamp}.html")
        jira.add_attachment_to_ticket(f"brussels_fr_main_{timestamp}.html")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
