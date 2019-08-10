from selenium import webdriver as wd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import HtmlTestRunner
import unittest



class YoutSearch(unittest.TestCase):

    def setUp(self):
        self.driver = wd.Chrome("./Drivers/chromedriver.exe")
        self.driver.get('https://youtube.com')
        self.driver.maximize_window()


    def test_search_youtube(self):
        driver = self.driver
        se = WebDriverWait(driver, 10).until(lambda dv: driver.find_element_by_xpath('(//input[contains(@id,"search")])[1]'))
        se.send_keys('all out life')
        seb = WebDriverWait(driver, 10).until(lambda dv: driver.find_element_by_xpath("/html//button[@id='search-icon-legacy']"))
        seb.click()
        # video = WebDriverWait(driver, 20, poll_frequency=3, ignored_exceptions=NoSuchElementException).until(lambda dv: driver.find_element_by_xpath('//*[@id="video-title"]'))
        video = WebDriverWait(driver, 20, poll_frequency=3, ignored_exceptions=NoSuchElementException).until(
            lambda dv: driver.find_element_by_xpath('//*[@id="video-title"]'))
        video.click()
        WebDriverWait(driver, 20)

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':

    testRunner = HtmlTestRunner.HTMLTestRunner(output="C:\SDriver")
    unittest.main(testRunner)








