"""
test every link
"""
from Pages import MortageCalculator
from selenium import webdriver as wd
import requests


class TestLinks:

    def test_check_Links(self):
        driver = wd.Chrome(executable_path="../Drivers/chromedriver.exe")
        home = MortageCalculator.MortgageCalculator(driver, "finance/how-much-house-can-i-afford.html#")
        home.open_page("Max")
        links = home.driver.find_elements_by_xpath("//*[@href]")
        for link in links:
            urlCheck = requests.head(link.get_attribute("href")).status_code
            if urlCheck == 999:
                    pass
            else:
                    self.assertLess(urlCheck, 400, "the url %s  is not valid error code %i" % (link.get_attribute("href"), urlCheck))



