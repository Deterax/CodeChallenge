from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
from selenium.webdriver.common.by import By

class GenericActions(object):

    def __init__(self, selen_dirver, main_url):
        self.driver = selen_dirver
        self.main_url = main_url

    def get_current_driver(self):
        return self.driver

    def get_current_url(self):
        return self.driver.current_url

    def find_by_xpath(self, where_to):
        # fine a given element
        return self.driver.find_element(By.XPATH, where_to)

    def open_page(self, resolution):
        url = self.main_url
        self.driver.get(url)
        if resolution is 'Max':
            self.driver.maximize_window()
        else:
            numbers = resolution.split("x")
            self.driver.set_window_size(numbers[0], numbers[1])

    def click_elm(self, where_to):
        elm = self.find_by_xpath(where_to)
        elm.click()

    def drag_something (self, full_slider, slider, to_where):
        #for slider move the knot not the slider completly, it moves it first to minimum, then to the desire percentage
        drag = ActionChains(self.driver)
        drag.click_and_hold(slider).move_by_offset(-full_slider.size['width'], 0).release().perform()
        drag.release(slider)
        width_value = int(full_slider.size['width']*(to_where/100))
        drag.click_and_hold(slider).move_by_offset(width_value, 0).release().perform()
        drag.release(slider)
        drag.reset_actions()


