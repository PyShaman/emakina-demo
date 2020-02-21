import re
import requests


def get_data_from_xml_sitemap(url):
    response = requests.get(f"{url}/sitemap.xml", verify=False).content.decode("utf-8")
    results = re.findall("https://[a-z./-]*", response)
    return results
