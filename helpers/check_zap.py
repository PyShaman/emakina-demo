import requests
from retrying import retry


@retry(stop_max_delay=120000)
def check_zap_connection(host, port):
    return requests.get(f"{host}:{port}/").status_code
