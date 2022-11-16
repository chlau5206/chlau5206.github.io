# Selenium Test 01 -- simple test 
import os
import time
import unittest
import sys

from SeleniumSetup import SeleniumWebDriver
from TestSuite01 import Suite01

###############################################
# // run test cases
################################################

if __name__ == "__main__":
    selenium = SeleniumWebDriver()
    driver = selenium.getDriver("FireFox")
    #driver = selenium.getDriver("Opera")
    #baseURL = r"file:///E:/[GitHub-Repos]/chlau5206.github.io/index.html"
    baseURL = r"https://www.google.com"

    suit = Suite01(driver, baseURL)

    suit.TestCase01()
    suit.TestCase02()
    
    driver.close()
    #driver.quit()

