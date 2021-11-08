from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random
from modules.table_tool import TablesTool


class ScrapeBot:

    '''
        This module is doing the actual work of scraping the data from Facebook.
        1. It logs in
        2. It visits the chosen ad accounts and extracts the billing info

        It uses the Selenium Framework and Chrome Driver to manipulate the browser and simulate
        human behaviour.
    '''

    #Each instance is a separate chrome session.
    def __init__(self,driver_dir):
        self.driver= webdriver.Chrome(driver_dir)

    # This method is responsible for logging in to Facebook. It is designed to work with Two-Factor Authentication
    # It enters the user info and then it enters the authentication code ( Google Authenticator)#
    # The time between each action is chosen randomly every time, so it resembles a real human behaviour.
    def login_to_fb(self, url, username, password , two_factor_key):
        self.driver.get(url)
        policy_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='cookie-policy-dialog-accept-button']")
        time.sleep(random.randint(1,4))
        policy_button.click()
        time.sleep(random.randint(2, 4))
        email_input = self.driver.find_element(By.CSS_SELECTOR, "input#email")
        pass_input = self.driver.find_element(By.CSS_SELECTOR, "input#pass")
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button#loginbutton")
        email_input.send_keys(username)
        time.sleep(random.randint(2,5))
        pass_input.send_keys(password)
        time.sleep(random.randint(1,3))
        login_button.click()
        time.sleep(random.randint(4,8))
        two_factor_input = self.driver.find_element(By.CSS_SELECTOR, "input#approvals_code")
        submit_key_button = self.driver.find_element(By.CSS_SELECTOR, "button#checkpointSubmitButton")
        secret_code = two_factor_key
        two_factor_input.send_keys(secret_code)
        submit_key_button.click()
        time.sleep(random.randint(7,13))

    def get_url(self, url):
        self.driver.get(url)

    # This method is doing the scraping after the bot has logged in to Facebook.
    def scrape_invoices_info(self):
        time.sleep(random.randint(7,12))
        parent_element = self.driver.find_element(By.XPATH,
                                             "//div[text()='Transaction ID']/parent::*/parent::*/parent::*/parent::*")
        child_element = parent_element.find_elements(By.XPATH, "./*")
        info = []
        for el in child_element:
            formated_text = el.text.replace(',', ".")
            formated_text = formated_text.replace("\n", ",")
            formated_text = formated_text.split(",")
            info.append(formated_text)
        return info[1:]

    def close(self):
        self.driver.close()
