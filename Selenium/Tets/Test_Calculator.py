"""
data test on calculator
"""
from Pages.MortageCalculator import MortgageCalculator
import unittest
from selenium import webdriver as wd
import random
from Tets.sharedTest import SharedTest
from selenium.webdriver.common.keys import Keys


class CalculatorsTest(unittest.TestCase):

    def setUp(self):
        driver = wd.Chrome(executable_path="../Drivers/chromedriver.exe")
        self.home = MortgageCalculator(driver, "finance/how-much-house-can-i-afford.html#")
        self.home.open_page("Max")
        self.home.set_mid_values()

    def test_annual_field_invalid(self):
        #test for invalid value
        self.home.find_by_xpath(self.home.annual_income_input).send_keys(random.randint(500000, 1000000))
        self.home.set_input_value(self.home.time_input, "20")
        assert self.home.find_by_xpath(self.home.annual_income_input).get_property("value") == "500,000"
        SharedTest.test_consistency(self)

    def test_annual_field_valid(self):
        #test for invalid value
        random_number = random.randint(0, 500000)
        self.home.find_by_xpath(self.home.annual_income_input).send_keys(random_number)
        self.home.set_input_value(self.home.time_input, "20")
        assert int(self.home.find_by_xpath(self.home.annual_income_input).get_property("value").replace(',', '')) == random_number
        SharedTest.test_consistency(self)

    def test_interest_invalid(self):
        #test for invalid value
        self.home.find_by_xpath(self.home.interest_input).send_keys(random.randint(11, 100))
        self.home.set_input_value(self.home.time_input, "20")
        assert self.home.find_by_xpath(self.home.interest_input).get_property("value") == "10"
        SharedTest.test_consistency(self)

    def test_interest_valid(self):
        #test for valid value
        random_number = round(random.uniform(0, 10), 1)
        self.home.find_by_xpath(self.home.interest_input).send_keys(str("{:.1f}".format(random_number)))
        self.home.set_input_value(self.home.time_input, "20")
        random_number = str("{:.1f}".format(random_number))
        assert self.home.find_by_xpath(self.home.interest_input).get_property("value") == random_number
        SharedTest.test_consistency(self)

    def test_down_Payment_invalid(self):
        #test for invalid value
        self.home.find_by_xpath(self.home.downpay_input).send_keys(random.randint(270001, 1000000))
        self.home.set_input_value(self.home.time_input, "20")
        assert self.home.find_by_xpath(self.home.downpay_input).get_property("value") == "270,000"
        SharedTest.test_consistency(self)

    def test_down_Payment_valid(self):
        #test for invalid value
        random_number = random.randint(0, 270000)
        self.home.find_by_xpath(self.home.downpay_input).send_keys(random_number)
        self.home.set_input_value(self.home.time_input, "20")
        assert int(self.home.find_by_xpath(self.home.downpay_input).get_property("value").replace(',', '')) == random_number
        SharedTest.test_consistency(self)

    def test_time_invalid(self):
        #test for invalid value
        self.home.find_by_xpath(self.home.time_input).send_keys(random.randint(41, 1000))
        self.home.set_input_value(self.home.annual_income_input, "240000")
        assert self.home.find_by_xpath(self.home.time_input).get_property("value") == "40"
        SharedTest.test_consistency(self)

    def test_time_valid(self):
        #test for valid value
        random_number = random.randint(15, 40)
        self.home.find_by_xpath(self.home.time_input).send_keys(random_number)
        self.home.find_by_xpath(self.home.time_input).send_keys(Keys.RETURN)
        self.home.set_input_value(self.home.annual_income_input, "240000")
        print(random_number)
        print(self.home.find_by_xpath(self.home.time_input).get_property("value"))
        assert self.home.find_by_xpath(self.home.time_input).get_property("value") == random_number
        SharedTest.test_consistency(self)

    def test_Monthly_Payment_affordable(self):
        #initial values to mid range, affordable limit point<5700, or 57%of slide
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 30)
        # assert for dispaly of gren track
        assert self.home.find_by_xpath(self.home.slider_left_selection_green).is_displayed()
        # get if it is affordable or not
        assert self.home.is_affordable()

    def test_Monthly_Payment_not_affordable(self):
        #initial values to mid range, affordable limit point<5700, or 57%of slide
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 90)
        # assert for dispaly of gren track
        assert self.home.find_by_xpath(self.home.slider_left_selection_green).is_displayed()
        # get if it is affordable or not
        assert not self.home.is_affordable()

    def test_slide_annual_min(self):

        self.home.drag_something(self.home.find_by_xpath(self.home.full_annual_income_slide),
                                 self.home.find_by_xpath(self.home.annual_income_slide), 0)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 50)
        assert not self.home.is_affordable()
        #SharedTest.test_consistency(self)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 0)
        assert self.home.is_affordable()
        assert not self.home.find_by_xpath(self.home.slider_left_selection_green).is_displayed()

    def test__slide_annual_max(self):
        self.home.drag_something(self.home.find_by_xpath(self.home.full_annual_income_slide),
                                 self.home.find_by_xpath(self.home.annual_income_slide), 100)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 50)
        assert not self.home.is_affordable()
        SharedTest.test_consistency(self)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 0)
        assert self.home.is_affordable()
        SharedTest.test_consistency(self)

    def test_slide_interest_min(self):
        self.home.drag_something(self.home.find_by_xpath(self.home.interest_slide_track),
                                 self.home.find_by_xpath(self.home.interest_slide), 0)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 50)
        assert self.home.find_by_xpath(self.home.max_amount).text == "0"
        assert self.home.is_affordable()
        SharedTest.test_consistency(self)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 90)
        assert not self.home.is_affordable()
        SharedTest.test_consistency(self)

    def test__slide_interest_max(self):
        self.home.drag_something(self.home.find_by_xpath(self.home.interest_slide_track),
                                 self.home.find_by_xpath(self.home.interest_slide), 100)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 50)
        assert self.home.is_affordable()
        SharedTest.test_consistency(self)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 90)
        assert not self.home.is_affordable()
        SharedTest.test_consistency(self)

    def test_slide_down_pay_min(self):
        self.home.drag_something(self.home.find_by_xpath(self.home.down_pay_slide_track),
                                 self.home.find_by_xpath(self.home.down_pay_slide), 0)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 50)
        assert self.home.is_affordable()
        SharedTest.test_consistency(self)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 0)
        assert self.home.is_affordable()
        SharedTest.test_consistency(self)

    def test_slide_down_pay_max(self):
        self.home.drag_something(self.home.find_by_xpath(self.home.down_pay_slide_track),
                                 self.home.find_by_xpath(self.home.down_pay_slide), 100)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 50)
        assert self.home.is_affordable()
        SharedTest.test_consistency(self)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 0)
        assert self.home.is_affordable()
        SharedTest.test_consistency(self)

    def test_slide_time_min(self):
        self.home.drag_something(self.home.find_by_xpath(self.home.time_slide_track),
                                 self.home.find_by_xpath(self.home.time_slide), 0)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 50)
        assert self.home.find_by_xpath(self.home.max_amount).text == "684,200"
        assert self.home.is_affordable()
        SharedTest.test_consistency(self)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 90)
        assert not self.home.is_affordable()
        SharedTest.test_consistency(self)

    def test_slide_time_max(self):
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 50)
        self.home.drag_something(self.home.find_by_xpath(self.home.time_slide_track),
                                 self.home.find_by_xpath(self.home.time_slide), 100)
        self.home.find_by_xpath(self.home.time_input).send_keys(Keys.RETURN)
        print(self.home.find_by_xpath(self.home.max_amount).text)
        assert self.home.find_by_xpath(self.home.max_amount).text == "969,200"
        assert self.home.is_affordable()
        SharedTest.test_consistency(self)
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 90)
        assert not self.home.is_affordable()
        SharedTest.test_consistency(self)

    def test_slide_month_pay_min(self):
        #initial values to mid range, affordable limit point<5700, or 57%of slide
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 0)
        # assert for dispaly of gren track
        assert self.home.find_by_xpath(self.home.slider_left_selection_green).is_displayed()
        # get if it is affordable or not
        assert self.home.is_affordable()

    def test__slide_moth_pay_max(self):
        #initial values to mid range, affordable limit point<5700, or 57%of slide
        self.home.drag_something(self.home.find_by_xpath(self.home.full_slider_track),
                                 self.home.find_by_xpath(self.home.monthpay_slide), 100)
        # assert for dispaly of gren track
        assert self.home.find_by_xpath(self.home.slider_left_selection_green).is_displayed()
        # get if it is affordable or not
        assert not self.home.is_affordable()


    def tearDown(self):
        self.home.driver.close()



if __name__ == '__main__':
    unittest.main()




