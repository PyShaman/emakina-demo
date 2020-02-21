import os
import datetime
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from access.check import AxeEngine
from data.get_data_from_url import get_data_from_xml_sitemap

timestamp = str(datetime.datetime.now().isoformat()).replace(":", "-")[:10]


class TestAccessibility:

    @pytest.fixture()
    def test_setup(self):
        global driver
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--enable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        yield
        driver.quit()

    @staticmethod
    def test_prepare_directory():
        try:
            os.mkdir(f"results/{timestamp}_all")
            os.mkdir(f"results/{timestamp}_all/flanders_nl")
            os.mkdir(f"results/{timestamp}_all/brussels_fr")
        except OSError:
            print(f"Creation of the directory {timestamp} failed")
        else:
            print(f"Successfully created the directory {timestamp}")

    @staticmethod
    def test_all_sites_flanders_nl(test_setup):
        ae = AxeEngine()
        results = get_data_from_xml_sitemap("https://www.servicevoucher-vl-nl.acc.sodexo.be")
        for result in results:
            site_name = result[47:]
            driver.get(result)
            ae.inject_all_rules(driver, timestamp, "flanders_nl", f"flanders_nl_{site_name}.txt", result)

    @staticmethod
    def test_all_sites_wallonie_fr(test_setup):
        ae = AxeEngine()
        results = get_data_from_xml_sitemap("https://www.servicevoucher-bl-fr.acc.sodexo.be")
        for result in results:
            site_name = result[47:]
            driver.get(result)
            ae.inject_all_rules(driver, timestamp, "brussels_fr", f"brussels_fr{site_name}.txt", result)
