import contextlib
import json
import os
import time

import keyring
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver

TIME_TRACK_BASE_URL = os.environ["TIME_TRACK_BASE_URL"]


def get_access_token(email=None, password=None, headless=False):
    if email and password:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        drive = webdriver.Chrome(
            options=chrome_options, seleniumwire_options={"disable_encoding": True}
        )
    else:
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        drive = webdriver.Chrome(
            seleniumwire_options={"disable_encoding": True}, options=chrome_options
        )

    with contextlib.closing(drive) as driver:
        driver.get(TIME_TRACK_BASE_URL)
        if email and password:
            wait_email = ui.WebDriverWait(driver, 60)  # timeout after 120 seconds
            wait_email.until(
                lambda driver: driver.find_element(By.CSS_SELECTOR, "#i0116")
            )
            email_input = driver.find_element(By.CSS_SELECTOR, "#i0116")
            email_input.send_keys(email)
            email_input.send_keys(Keys.ENTER)

            wait_password = ui.WebDriverWait(driver, 60)  # timeout after 120 seconds
            wait_password.until(
                lambda driver: driver.find_element(By.CSS_SELECTOR, "#i0118")
            )
            password_input = driver.find_element(By.CSS_SELECTOR, "#i0118")
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
            password_input.send_keys(Keys.ENTER)

            time.sleep(2)
            sign_in = driver.find_element(By.CSS_SELECTOR, "#idSIButton9")
            sign_in.click()

            time.sleep(2)
            code = driver.find_element(By.CSS_SELECTOR, "#idRichContext_DisplaySign")
            print("Insert this code in the Authenticator App 👉", code.text)

        wait_login = ui.WebDriverWait(driver, 1000)  # timeout after 120 seconds
        wait_login.until(
            lambda driver: driver.find_element(By.ID, "panel-1010-innerCt")
        )
        for request in driver.requests:
            if request.response:
                if "load_all_ext" in request.url:
                    body = request.response.body
                    data = json.loads(str(body, "utf-8"))
                    access_token = data["userData"]["accessToken"]
                    keyring.set_password("system", "timetoc_access_token", access_token)
                    print("🔑 Access token obtained and saved!")
                    return access_token
