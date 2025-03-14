from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re

from helping_functions import clean_url


def get_eta(preprocessed_route_url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(preprocessed_route_url)

    page_source = driver.page_source
    driver.quit()

    match = re.search(r">([^<>]*\d+h(?:\s+\d+m)?|\d+\s*min)<", page_source)
    if match:
        eta = match.group(1)
        return eta

    return None


print(get_eta(clean_url("https://maps.app.goo.gl/xmCWvzE18CuutHsd8?g_st=ac")))