from selenium import webdriver
from time import sleep
import os
import webbrowser
import json

with open("data.json") as f:
    _data = json.load(f)

DOWNLOAD_DIR = os.path.abspath("./result")

FILES_BEFORE = len(os.listdir(DOWNLOAD_DIR))

SRF_NO = _data["SRF_NO"]

MOBILE_NO = _data["MOBILE_NO"]

POLLING_RATE = max(_data.get("POLLING_RATE", 60), 10)

URL = "https://labsys.health.kerala.gov.in/Download_report/patient_test_report"


def check_fail(driver: webdriver.Firefox):
    style = driver.find_elements_by_class_name("sweet-overlay")
    return len(style) != 0


def show_result():
    existing_files = os.listdir(DOWNLOAD_DIR)
    while len(existing_files) == FILES_BEFORE:
        sleep(1)
        existing_files = os.listdir(DOWNLOAD_DIR)
        
    files = [x for x in existing_files if x.endswith(".pdf")]
    newest = max([os.path.join(DOWNLOAD_DIR, file) for file in files], key=os.path.getctime)
    webbrowser.open(newest)


def load_driver() -> webdriver.Firefox:
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", DOWNLOAD_DIR)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    profile.set_preference("pdfjs.disabled", True)

    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")

    return webdriver.Firefox(profile, options=options)

try:
    os.mkdir(DOWNLOAD_DIR)
except FileExistsError:
    pass

browser = load_driver()

while True:
    browser.get(URL)

    browser.find_element_by_name("srf_id").send_keys(SRF_NO)

    browser.find_element_by_name("mobile").send_keys(MOBILE_NO)

    captcha = browser.find_element_by_id("mainCaptcha_login1").get_attribute("innerText")

    browser.find_element_by_id("txtinput1").send_keys(captcha)

    browser.find_element_by_id("generate_pdf").click()

    if not check_fail(browser):
        break
    
    sleep(POLLING_RATE)

show_result()
browser.close()
