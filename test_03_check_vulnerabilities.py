import time
import unittest
import security.zap as security
from selene.api import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class TestVulnerabilities(unittest.TestCase):
    zap = security.Zap()
    zap.start_zap()
    print("Checking connection to localhost")
    zap.check_zap_connection()
    print("connected to localhost")
    zap.start_passive_scan()

    @classmethod
    def setUpClass(cls):
        proxy_host = "127.0.0.1"
        proxy_port = 8096
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--headless")
        options.add_argument(f"--proxy-server={proxy_host}:{proxy_port}")
        browser.set_driver(webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options))
        time.sleep(10)

    @classmethod
    def tearDownClass(cls):
        zap = security.Zap()
        browser.quit()
        zap.stop_zap()

    @staticmethod
    def test_flanders_nl_main_site_for_vulnerabilities():
        zap = security.Zap()
        # browser.open_url("https://www.servicevoucher-vl-nl.acc.sodexo.be")
        zap.run_spider("https://www.servicevoucher-vl-nl.acc.sodexo.be")

    @staticmethod
    def test_brussels_fr_main_site_for_vulnerabilities():
        zap = security.Zap()
        # browser.open_url("https://www.servicevoucher-bl-fr.acc.sodexo.be")
        zap.run_spider("https://www.servicevoucher-bl-fr.acc.sodexo.be")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
