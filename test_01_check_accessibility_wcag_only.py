import datetime
import unittest
import os
import shutil
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from access.check import AxeEngine
from data.get_data_from_url import get_data_from_xml_sitemap
from data.jira_access import Jira

timestamp = str(datetime.datetime.now().isoformat()).replace(":", "-")[:10]


class TestAccessibilityWCAGOnly(unittest.TestCase):

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
        os.remove(f"wcag2a_{timestamp}.zip")
        os.remove(f"wcag2aa_{timestamp}.zip")

    @staticmethod
    def test_01_prepare_directory():
        try:
            os.mkdir(f"results/{timestamp}_wcag2a")
            os.mkdir(f"results/{timestamp}_wcag2a/flanders_nl")
            os.mkdir(f"results/{timestamp}_wcag2a/brussels_fr")
            os.mkdir(f"results/{timestamp}_wcag2aa")
            os.mkdir(f"results/{timestamp}_wcag2aa/flanders_nl")
            os.mkdir(f"results/{timestamp}_wcag2aa/brussels_fr")

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
            ae.inject_only_wcag2a(driver, timestamp, "flanders_nl", f"flanders_nl_{site_name}.txt", result)
            ae.inject_only_wcag2aa(driver, timestamp, "flanders_nl", f"flanders_nl_{site_name}.txt", result)

    @staticmethod
    def test_03_all_sites_brussels_fr():
        ae = AxeEngine()
        results = get_data_from_xml_sitemap("https://www.servicevoucher-bl-fr.acc.sodexo.be")
        for result in results:
            site_name = result[47:]
            driver.get(result)
            ae.inject_only_wcag2a(driver, timestamp, "brussels_fr", f"brussels_fr{site_name}.txt", result)
            ae.inject_only_wcag2aa(driver, timestamp, "brussels_fr", f"brussels_fr{site_name}.txt", result)

    @staticmethod
    def test_04_zip_results():
        shutil.make_archive(f"wcag2a_{timestamp}", "zip", f"results/{timestamp}_wcag2a")
        shutil.make_archive(f"wcag2aa_{timestamp}", "zip", f"results/{timestamp}_wcag2aa")

    @staticmethod
    def test_05_send_report_to_jira():
        jira = Jira()
        jira.create_issue("Accessibility testing WCAG2A, AA", "Accessibility testing report WCAG2A, AA", timestamp)
        jira.add_attachment_to_ticket(f"wcag2a_{timestamp}.zip")
        jira.add_attachment_to_ticket(f"wcag2aa_{timestamp}.zip")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
