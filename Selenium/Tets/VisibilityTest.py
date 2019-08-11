"""
testVisibility
1.test resolution: 1366x768
2.test resolution: 1920x1080
3.test resolution: 1440x900
4.test resolution: 1280x720
"""
from Pages import MortageCalculator
from selenium import webdriver as wd


class TestVisibility:

    def open_resolution(self, Resolution):
        resolutions = ["1366x768", "1920x1080", "1440x900", "1280x720"]
        driver = wd.Chrome(executable_path="C:\SDriver\chromedriver.exe")
        home = MortageCalculator.MortgageCalculator(driver, "finance/how-much-house-can-i-afford.html#")
        for res in resolutions:
            home.open_page(res)




