import time
import unittest
import security.zap as security
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

    @staticmethod
    def test_01_flanders_nl_main_site_for_vulnerabilities():
        zap = security.Zap()
        zap.run_spider("https://www.servicevoucher-vl-nl.acc.sodexo.be")

    @staticmethod
    def test_02_brussels_fr_main_site_for_vulnerabilities():
        zap = security.Zap()
        zap.run_spider("https://www.servicevoucher-bl-fr.acc.sodexo.be")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
