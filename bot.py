from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class Website:
    def __init__(self, username, password):
        self.xpath = "/html/body/div[4]/div[2]/div/div[2]/div/div/div[3]/div/div[2]/span/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/form/div/div[1]/div/div[2]/div/div/div/fieldset/ul/li[1]/div/div/div/div/label/div/div/span[1]/div/span/div"
        self.url = "https://www.khanacademy.org/login"
        self.username = username
        self.password = password

        self.driver = webdriver.Chrome("C:\\chromedriver.exe")
        self.driver.get(self.url)

    def wait_for_element(self, xpath):
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            print("Loading took too much time!")
            return False

    def login(self):
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div/div[2]/div/div[3]/section[2]/div/div/div[2]/div[2]/form/input").send_keys(
            self.username)
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div/div[2]/div/div[3]/section[2]/div/div/div[2]/div[3]/form/input").send_keys(
            self.password)
        self.driver.find_element_by_xpath(
            "/html/body/div[2]/div[3]/div/div[2]/div/div[3]/section[2]/div/div/div[2]/button").click()

    def goto_quiz(self):
        # click economics section than click resume first quiz than clicks lets go button
        self.driver.get("https://www.khanacademy.org/economics-finance-domain/microeconomics/basic-economic-concepts-gen-micro/economics-introduction/e/scarcity?modal=1")
        self.wait_for_element("/html/body/div[4]/div[2]/div/div[2]/div/div/div[3]/div/div[2]/span/div/div/div[1]/div/div[2]/div[3]/div/button")
        self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[2]/div/div/div[3]/div/div[2]/span/div/div/div[1]/div/div[2]/div[3]/div/button").click()

    def answer(self):
        xpath_check_button = "/html/body/div[4]/div[2]/div/div[2]/div/div/div[3]/div/div[2]/span/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div[2]/button"

        # while wrong text is present
        correct = 0
        index = 1
        do = True
        while do or (self.driver.find_element_by_xpath(xpath_check_button).text == "Check again") or (self.driver.find_element_by_xpath(xpath_check_button).text == "Check"):
            do = False
            print(self.xpath)
            self.driver.find_element_by_xpath(self.xpath).click()
            self.driver.find_element_by_xpath(xpath_check_button).click()

            if self.driver.find_element_by_xpath(xpath_check_button).text == "Next question":
                correct += 1
                print(f"Correct! Number: {correct}")

                replaceable = index
                index = 1
                self.xpath = self.xpath.replace("li[" + str(replaceable) + "]", "li[" + str(index) + "]")
                self.driver.find_element_by_xpath(xpath_check_button).click()
                do = True
            else:
                replaceable = index
                index += 1
                self.xpath = self.xpath.replace("li[" + str(replaceable) + "]", "li[" + str(index) + "]")
                self.driver.find_element_by_xpath(xpath_check_button).click()

        time.sleep(4)
        self.driver.close()


Website = Website("username", "password")
Website.wait_for_element("/html/body/div[2]/div[3]/div/div[2]/div/div[3]/section[2]/div/div/div[2]/div[2]/form/input")
Website.login()
time.sleep(5)
Website.goto_quiz()
time.sleep(2)
Website.answer()
