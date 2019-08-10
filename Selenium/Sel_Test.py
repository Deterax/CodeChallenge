from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import unittest
import urllib.request


driver = wd.Chrome(executable_path="C:\SDriver\chromedriver.exe")

driver.get('https://youtube.com')
driver.maximize_window()
se = WebDriverWait(driver, 10).until(lambda dv: driver.find_element_by_xpath('(//input[contains(@id,"search")])[1]'))
se.send_keys('all out life')
seb = WebDriverWait(driver, 10).until(lambda dv: driver.find_element_by_id('search-icon-legacy'))
seb.click()
links = driver.find_elements_by_xpath('//*[@href]')
for link in links:
    if (urllib.request.urlopen("http://www.stackoverflow.com").getcode()==200):
        print('valid')
    else:
        print('invalid')


