"""
shared test action
"""
from Pages.MortageCalculator import MortgageCalculator
import unittest
from selenium import webdriver as wd
from selenium.webdriver.support.color import Color
import requests


class SharedTest(unittest.TestCase):

    def setUp(self):
        driver = wd.Chrome(executable_path="../Drivers/chromedriver.exe")
        self.home = MortgageCalculator(driver, "finance/how-much-house-can-i-afford.html#")
        self.home.open_page("Max")
        self.home.set_mid_values()

    def test_consistency(self):
        # testing other fields and consistency
        # place monthly to  mid range
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 50)
        # assert for dispaly of gren track
        assert self.home.find_by_xpath(self.home.slider_left_selection_green).is_displayed()
        # get if it is affordable or not
        if self.home.is_affordable():
            max_amount = self.home.find_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not self.home.find_by_xpath(self.home.alt_message).is_displayed()
            assert self.home.find_by_xpath(self.home.success_pig).is_displayed()
            assert not self.home.find_by_xpath(self.home.fail_pig).is_displayed()
        else:
            max_amount = self.home.find_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert self.home.find_by_xpath(self.home.alt_message).is_displayed()
            assert not self.home.find_by_xpath(self.home.success_pig).is_displayed()
            assert self.home.find_by_xpath(self.home.fail_pig).is_displayed()

    def test_check_Links(self):
        links = self.home.driver.find_elements_by_xpath("//*[@href]")
        for link in links:
            urlCheck = requests.head(link.get_attribute("href")).status_code
            if urlCheck == 999:
                    pass
            else:
                    self.assertLess(urlCheck, 400, "the url %s  is not valid error code %i" % (link.get_attribute("href"), urlCheck))


    def tearDown(self):
        self.home.driver.close()


if __name__ == '__main__':
    unittest.main()




