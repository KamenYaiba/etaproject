from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re



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

print(get_eta("https://www.google.com/maps/dir/39.8234879,-106.1595467/Eureka+Mountain,+%D9%83%D9%88%D9%84%D9%88%D8%B1%D8%A7%D8%AF%D9%88+81252%D8%8C+%D8%A7%D9%84%D9%88%D9%84%D8%A7%D9%8A%D8%A7%D8%AA+%D8%A7%D9%84%D9%85%D8%AA%D8%AD%D8%AF%D8%A9%E2%80%AD/@38.0640375,-104.9724097,9.25z/?hl=en"))