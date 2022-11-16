## Test suite 01 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


from time import sleep
#import Pylance


class Suite01: 
    def __init__(self, webDriver, baseURL):
        self.driver = webDriver
        self.baseURL = baseURL
    
    def TestCase01(self):
        self.driver.get(self.baseURL)
        expectedTitle = "Home page - ChLau 5206 GitHub"
        if (expectedTitle in self.driver.title):
            print("TC01: Pass")
        else:
            print("TC01: Fail")
        # sleep(3)

    def TestCase02(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(self.baseURL)
        elem = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, "q")))
        elem.send_keys("Flower Dance")
        elem.submit()
        print("TC02: Done")

        sleep(10)
        



