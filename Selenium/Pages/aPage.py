from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
from selenium.webdriver.common.by import By


class Page(object):

    def __init__(self, selen_dirver, added_url):
        # a website
        main_url = "https://www.consumeraffairs.com/"
        self.main_url = main_url+added_url
        self.driver = selen_dirver

    def change_url(self, url):
        self.main_url = self.main_url + url

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

    def get_text(self, locator):
        text = ''
        try:
            text = self.get_element(locator).text
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when getting text from the path-'%s'"%locator)
            return None
        else:
            return text.encode('utf-8')

    def select_dropdown_option(self, locator, option_text):

        result_flag = False
        try:
            dropdown = self.get_element(locator)
            for option in dropdown.find_elements_by_tag_name('option'):
                if option.text == option_text:
                    option.click()
                    result_flag = True
                    break
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when selecting option from the drop-down '%s' " % locator)

        return result_flag

    def click_elm(self, where_to):
        elm = self.find_by_xpath(where_to)
        elm.click()

    def write_something (self, where_to, what_to):
        try:
            wt = self.find_element(where_to)
            wt.clear()
            wt.send_keys(what_to)
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when getting text from the path-'%s'" % where_to)

    def drag_something (self, full_slider, slider, to_where):
        #for slider move the knot not the slider completly, it moves it first to minimum, then to the desire percentage
        drag = ActionChains(self.driver)
        drag.click_and_hold(slider).move_by_offset(-full_slider.size['width'], 0).release().perform()
        drag.release(slider)
        width_value = int(full_slider.size['width']*(to_where/100))
        drag.click_and_hold(slider).move_by_offset(width_value, 0).release().perform()
        drag.release(slider)
        drag.reset_actions()

    def set_input_value(self, which_to, amount):
        try:
            income = self.find_by_xpath(which_to)
        except Exception as e:
            self.write(e)
            self.exceptions.append("Error when finding from the path-'%s'" % which_to)
            return None
        else:
            income.send_keys(amount)



    def tearDown(self):
        self.driver.close()




