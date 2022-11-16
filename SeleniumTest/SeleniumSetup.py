# Setup Selenium 
import os
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver import chromium
# from selenium.webdriver import Chrome
# from selenium.webdriver import Edge

class SeleniumWebDriver:
    def getFirefoxdriver(self):
        binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        driver_location = r"C:\ProgramData\Anaconda3\geckodriver.exe" # 32-bit driver
        GitHub_driver_location = r"C:\SeleniumWebDrivers\GeckoDriver\geckodriver.exe"
        # executable_path = driver_location

        #driverLocation = r"C:\Users\chlau\AppData\Roaming\Python\Python39\site-packages\selenium\webdriver\geckodriver.exe"
        #opts.add_argument('--start-maximized')
        #opts.add_argument("--headless")
        opts = webdriver.FirefoxOptions()
        opts.binary_location = binary_location
        opts.add_argument("--width=800")
        opts.add_argument("--height=600")
        opts.page_load_strategy = 'normal'
        caps = webdriver.DesiredCapabilities().FIREFOX
        #caps["marionette"] = True
        #self.driver = Firefox(capabilities=caps,options=opts)
        driver = Firefox(executable_path=GitHub_driver_location, capabilities=caps, options=opts)

        return self.driver
    
    # def getOperaDriver(self):  # under construction
    #     #capabilities = webdriver.DesiredCapabilities()
    #     binary_location = r"C:\Users\chlau\AppData\Local\Programs\Opera\launcher.exe"
    #     driver_location = r"C:\ProgramData\Anaconda3\operadriver.exe" # 32-bit driver
        
    #     opts = webdriver.ChromeOptions()
    #     opts.binary_location = binary_location
    #     opts.add_argument("--width=800")
    #     opts.add_argument("--height=600")
    #     opts.page_load_strategy = 'normal'
    #     caps = webdriver.DesiredCapabilities().CHROME
    #     caps["platform"] = "WINDOWS"
    #     # caps["browserName"] = "Opera"
    #     # caps["marionette"] = True
    #     # aps["location"] = driver_location
    #     # self.driver = webdriver.Chrome(options=opts, executable_path=driver_location)
    #     driver = webdriver.Chrome(executable_path=driver_location, capabilities=caps, options=opts)

    #     return self.driver


    def getDriver(self, browser):
    #     browser = os.environ.get('AVA_TEST_BROWSER', 'Firefox')

        if browser == 'FireFox':
            b = self.getFirefoxdriver()
        elif browser == 'IE':
            b = webdriver.Ie()
        # elif browser == 'Chrome':
        #     b = webdriver.Chrome()
        # elif browser == 'ChromiumEdge':
        #     b = webdriver.ChromiumEdge()
        # elif browser == 'Safari':
        #     b = webdriver.Safari()
        elif browser == 'Opera':
            b = self.getOperaDriver()
        # elif browser == 'Remote':
        #     b = webdriver.Remote()
        else:
            b = webdriver.Edge()
        b.implicitly_wait(5)

        return b  # select webDriver

  