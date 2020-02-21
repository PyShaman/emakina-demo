import time
import requests
from retrying import retry
from subprocess import Popen, DEVNULL
from zapv2 import ZAPv2
from datetime import datetime


class Zap:
    def __init__(self):
        self.localProxy = {
            "http": "http://127.0.0.1:8096",
            "https": "http://127.0.0.1:8096",
        }
        self.host = "http://127.0.0.1"
        self.port = "8096"
        self.apikey = "al75sdd15vubce6vtahhkcscjn"
        self.zap = ZAPv2(proxies=self.localProxy, apikey=self.apikey)
        self.core = self.zap.core
        self.spider = self.zap.spider
        self.ajax = self.zap.ajaxSpider
        self.ascan = self.zap.ascan
        self.applicationURL = []

    @staticmethod
    def start_zap():
        print("Starting ZAP Proxy")
        process = Popen(
            [r"C:\Program Files\OWASP\Zed Attack Proxy\zap.bat", "-silent"],
            cwd=r"C:\Program Files\OWASP\Zed Attack Proxy",
            stdin=None,
            stdout=DEVNULL,
            stderr=None,
            shell=True,
        )
        time.sleep(1)
        print("ZAP process id: " + str(process.pid))

    def stop_zap(self):
        print("Shutdown ZAP")
        self.core.shutdown(apikey=self.apikey)

    @retry(stop_max_delay=40000)
    def check_zap_connection(self):
        return requests.get(f"{self.host}:{self.port}/").status_code

    def start_passive_scan(self):
        print("Starting passive scan")
        self.zap.pscan.set_enabled(enabled=True, apikey=self.apikey)

    def run_spider(self, target):
        print("Starting Scans on target: " + target)
        spider_scan_id = self.spider.scan(
            url=target,
            maxchildren=None,
            recurse=True,
            contextname=None,
            subtreeonly=None,
        )
        print("Scan ID: " + spider_scan_id)
        # Give the Spider a chance to start
        time.sleep(2)
        while int(self.spider.status(spider_scan_id)) < 100:
            print("Spider progress " + self.spider.status(spider_scan_id) + "%")
            time.sleep(5)
        print("Spider scan completed")
        time.sleep(5)
        print("Saving HTML report to file")
        timestamp = str(datetime.now().isoformat()).replace(":", "-")[:-7]
        my_file = open(f"ZAP_scan_{timestamp}.html", "w")
        my_file.write(self.core.htmlreport(self.apikey))
        my_file.close()

    def run_ajax_spider(self, target):
        # Ajax Spider the target URL
        print("Start Ajax Spider -> " + self.ajax.scan(url=target, inscope=None))
        # Give the Ajax spider a chance to start
        time.sleep(10)
        while self.ajax.status != "stopped":
            print("Ajax Spider is " + self.ajax.status)
            time.sleep(5)
        for url in self.applicationURL:
            # Ajax Spider every url configured
            print(
                "Ajax Spider the URL: "
                + url
                + " -> "
                + self.ajax.scan(url=url, inscope=None)
            )
            # Give the Ajax spider a chance to start
            time.sleep(10)
            while self.ajax.status != "stopped":
                print("Ajax Spider is " + self.ajax.status)
                time.sleep(5)
        print("Ajax Spider scan completed")
        print("Saving HTML report to file")
        timestamp = str(datetime.now().isoformat()).replace(":", "-")
        my_file_ajax_spider = open(f"ZAP_ajax_spider_{timestamp}.html", "w")
        my_file_ajax_spider.write(self.core.htmlreport(self.apikey))
        my_file_ajax_spider.close()

    def run_active_scan(self, target):
        active_scan_id = self.zap.ascan.scan(
            url=target, recurse=True, inscopeonly=None, method=None, postdata=True
        )
        print("Start Active scan. Scan ID: " + str(active_scan_id))
        while int(self.ascan.status(active_scan_id)) < 100:
            print("Active Scan progress: " + self.ascan.status(active_scan_id) + "%")
            time.sleep(5)
        print("Active Scan completed")
        print("Saving HTML report to file")
        timestamp = str(datetime.now().isoformat()).replace(":", "-")
        my_file_active_scan = open(f"ZAP_ascan_{timestamp}.html", "w")
        my_file_active_scan.write(self.core.htmlreport(self.apikey))
        my_file_active_scan.close()
