"""
data test on calculator
"""
from Pages.MortageCalculator import MortgageCalculator
import unittest
from selenium import webdriver as wd
import random
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import re
from selenium.webdriver.support.color import Color
import requests


class CalculatorsTest(unittest.TestCase):

    def setUp(self):
        driver = wd.Chrome(executable_path="../Drivers/chromedriver.exe")
        #initial values to mid range
        self.home = MortgageCalculator(driver, "finance/how-much-house-can-i-afford.html#")
        self.home.open_page("Max")

    def test_check_Links(self):
        self.home.set_mid_values()
        links = self.home.driver.find_elements_by_xpath("//*[@href]")
        for link in links:
            urlCheck = requests.head(link.get_attribute("href")).status_code
            if urlCheck == 999:
                pass
            else:
                self.assertLess(urlCheck, 400, "the url %s  is not valid error code %i" % (link.get_attribute("href"), urlCheck))

    def test_annual_field_invalid(self):
        driver = self.home.driver
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("135000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        #test for invalid value
        annual.send_keys(random.randint(500000, 1000000))
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        annual_value = driver.find_element_by_xpath(self.home.annual_income_input)
        assert annual_value.get_property("value") == "500,000"
        #testing other fields and consistency
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width/2, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_annual_field_valid(self):
        driver = self.home.driver
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("135000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        # test for valid value
        random_number = random.randint(0, 500000)
        annual_value = driver.find_element_by_xpath(self.home.annual_income_input)
        annual_value.send_keys(random_number)
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        random_number = str(random_number)
        maxlen = len(random_number)
        if maxlen > 3:
            random_number = random_number[0:3] + "," + random_number[3:maxlen]
        assert annual_value.get_property("value") == random_number
        # testing other fields and consistency
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_interest_invalid(self):
        driver = self.home.driver
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("135000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        annual.send_keys("240000")
        #test for invalid value
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys(random.randint(10, 20))
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        annual_value = driver.find_element_by_xpath(self.home.annual_income_input)
        assert interest.get_property("value") == "10"
        # testing other fields and consistency
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if post2_value == []:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_interest_valid(self):
        driver = self.home.driver
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("135000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        annual_value = driver.find_element_by_xpath(self.home.annual_income_input)
        annual_value.send_keys("240000")
        # test for valid value
        random_number = round(random.uniform(0, 10), 1)
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys(str(random_number))
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        random_number = str("{:.1f}".format(random_number))
        assert interest.get_property("value") == random_number
        # testing other fields and consistency
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_down_Payment_invalid(self):
        driver = self.home.driver
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        annual.send_keys("240000")
        #test for invalid value
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys(random.randint(270001, 1000000))
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        assert dpayment.get_property("value") == "270,000"
        # testing other fields and consistency
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_down_Payment_valid(self): 
        driver = self.home.driver
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        annual_value = driver.find_element_by_xpath(self.home.annual_income_input)
        annual_value.send_keys("240000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        # test for valid value
        random_number = random.randint(0, 270000)
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys(random_number)
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        print(random_number)
        random_number = str(random_number)
        maxlen = len(random_number)
        print(random_number)
        if maxlen >= 3:
            random_number = random_number[:3] + "," + random_number[3:maxlen]
        print(random_number)
        assert dpayment.get_property("value") == random_number
        # testing other fields and consistency
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_time_invalid(self):
        driver = self.home.driver
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        annual.send_keys("240000")
        #test for invalid value
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys(random.randint(41, 1000))
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("240000")
        time = driver.find_element_by_xpath(self.home.time_input)
        assert time.get_property("value") == "40"
        # testing other fields and consistency
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_time_valid(self):
        driver = self.home.driver
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        annual_value = driver.find_element_by_xpath(self.home.annual_income_input)
        annual_value.send_keys("240000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        # test for valid value
        random_number = random.randint(15, 40)
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys(random_number)
        random_number = str(random_number)
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("240000")
        time = driver.find_element_by_xpath(self.home.time_input)
        assert time.get_property("value") == random_number
        # testing other fields and consistency
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()


    def test_Monthly_Payment_affordable(self):
        driver = self.home.driver
        #initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        annual.send_keys("240000")
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("135000")
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width/3, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    
    def test_Monthly_Payment_not_affordable(self):
        driver = self.home.driver
        # initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        annual.send_keys("240000")
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("240000")
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  90% of the track, or 9000 monthly
        drag.click_and_hold(monthly).move_by_offset(width*.9, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        print(str(post1_value))
        print(str(post2_value))
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_slide_annual_min(self):
        driver = self.home.driver
        # initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("240000")
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        #place Annual income slider at minimum range
        slider_annual_income = driver.find_element_by_xpath(self.home.annual_income_slide)
        full_annual_slide = driver.find_element_by_xpath(self.home.full_annual_income_slide)
        full_annual_slide = full_annual_slide.size
        width_annual_slide = full_annual_slide['width']
        drag.click_and_hold(slider_annual_income).move_by_offset(-width_annual_slide, 0).perform()
        drag.release(slider_annual_income)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test__slide_annual_max(self):
        driver = self.home.driver
        # initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("135000")
        # place Annual income slider at maximum range
        slider_annual_income = driver.find_element_by_css_selector("[class] .range_block:nth-of-type(1) .slider-horizontal [role='slider']:nth-of-type(5)")
        full_annual_slide = driver.find_element_by_xpath(self.home.full_annual_income_slide)
        full_annual_slide = full_annual_slide.size
        width_annual_slide = full_annual_slide['width']
        print(width_annual_slide)
        drag_annual = ActionChains(driver)
        drag_annual.click_and_hold(slider_annual_income).move_by_offset(-width_annual_slide, 0).perform()
        drag_annual.release(slider_annual_income)
        drag_annual.click_and_hold(slider_annual_income).move_by_offset(width_annual_slide, 0).perform()
        drag_annual.release(slider_annual_income)
        drag_annual.reset_actions()
        # place monthly at the min
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        drag_month = ActionChains(driver)
        drag_month.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        # place monthly to  mid range
        drag_month.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        # get if it is affordable or not
        # get limit values
        desire_pay = driver.find_element_by_xpath(self.home.monthpay_slide)
        desire_pay_value = desire_pay.get_attribute("style")
        desire_pay_value = re.findall("\d+.\d+", desire_pay_value)
        if not desire_pay_value:
            desire_pay = driver.find_element_by_xpath(self.home.monthpay_slide)
            desire_pay_value = desire_pay.get_attribute("style")
            desire_pay_value = re.findall("\d+", desire_pay_value)
        desire_pay_value = float(desire_pay_value[0])
        max_payment = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        max_payment_value = max_payment.get_attribute("style")
        max_payment_value = re.split(r":", max_payment_value)
        max_payment_value = max_payment_value[2]
        max_payment_value = re.findall("\d+.\d+", max_payment_value)
        if not max_payment_value:
            max_payment = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            max_payment_value = max_payment.get_attribute("style")
            max_payment_value = re.split(r":", max_payment_value)
            max_payment_value = max_payment_value[2]
            max_payment_value = re.findall("\d+", max_payment_value)
        max_payment_value = float(max_payment_value[0])
        # compare if they are affordable
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        assert slider_left_selection_green.is_displayed()
        if desire_pay_value <= max_payment_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_slide_interest_min(self):
        driver = self.home.driver
        # initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        annual.send_keys("240000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("240000")
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        #place interest slider at minimum range
        slider_interest_income = driver.find_element_by_xpath(self.home.interest_slide)
        full_interest_slide = driver.find_element_by_xpath(self.home.interest_slide_track)
        full_interest_slide = full_interest_slide.size
        width_interest_slide = full_interest_slide['width']
        drag.click_and_hold(slider_interest_income).move_by_offset(-width_interest_slide, 0).perform()
        drag.release(slider_interest_income)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test__slide_interest_max(self):
        driver = self.home.driver
        # initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("135000")
        #place interest slider at minimum range
        drag = ActionChains(driver)
        slider_interest_income = driver.find_element_by_xpath(self.home.interest_slide)
        full_interest_slide = driver.find_element_by_xpath(self.home.interest_slide_track)
        full_interest_slide = full_interest_slide.size
        width_interest_slide = full_interest_slide['width']
        drag.click_and_hold(slider_interest_income).move_by_offset(width_interest_slide, 0).perform()
        drag.release(slider_interest_income)
        # place monthly at the min
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        drag_month = ActionChains(driver)
        drag_month.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag_month.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_slide_down_pay_min(self):
        driver = self.home.driver
        # initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        annual.send_keys("240000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        #place Down Payment income slider at minimum range
        slider_down_pay_income = driver.find_element_by_xpath(self.home.down_pay_slide)
        full_down_pay_slide = driver.find_element_by_xpath(self.home.down_pay_slide_track)
        full_down_pay_slide = full_down_pay_slide.size
        width_down_pay_slide = full_down_pay_slide['width']
        drag.click_and_hold(slider_down_pay_income).move_by_offset(-width_down_pay_slide, 0).perform()
        drag.release(slider_down_pay_income)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test__slide_down_pay_max(self):
        driver = self.home.driver
        # initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        dpayment = driver.find_element_by_xpath(self.home.downpay_input)
        dpayment.send_keys("135000")
        # place Down Payment income slider at max range
        drag = ActionChains(driver)
        slider_down_pay_income = driver.find_element_by_xpath(self.home.down_pay_slide)
        full_down_pay_slide = driver.find_element_by_xpath(self.home.down_pay_slide_track)
        full_down_pay_slide = full_down_pay_slide.size
        width_down_pay_slide = full_down_pay_slide['width']
        drag.click_and_hold(slider_down_pay_income).move_by_offset(width_down_pay_slide, 0).perform()
        drag.release(slider_down_pay_income)
        # place monthly at the min
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        drag_month = ActionChains(driver)
        drag_month.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag_month.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_slide_time_min(self):
        driver = self.home.driver
        # initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        annual.send_keys("240000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        down_pay = driver.find_element_by_xpath(self.home.downpay_input)
        down_pay.send_keys("20")
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        #place time  slider at minimum range
        slider_time_income = driver.find_element_by_xpath(self.home.time_slide)
        full_time_slide = driver.find_element_by_xpath(self.home.time_slide_track)
        full_time_slide = full_time_slide.size
        width_time_slide = full_time_slide['width']
        drag.click_and_hold(slider_time_income).move_by_offset(-width_time_slide, 0).perform()
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test__slide_time_max(self):
        driver = self.home.driver
        # initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        annual.send_keys("240000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        down_pay = driver.find_element_by_xpath(self.home.downpay_input)
        down_pay.send_keys("20")
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        # place monthly to  mid range
        drag.click_and_hold(monthly).move_by_offset(width / 2, 0).release().perform()
        drag.release(monthly)
        # place time income slider at minimum range
        slider_time_income = driver.find_element_by_xpath(self.home.time_slide)
        full_time_slide = driver.find_element_by_xpath(self.home.time_slide_track)
        full_time_slide = full_time_slide.size
        width_time_slide = full_time_slide['width']
        drag.click_and_hold(slider_time_income).move_by_offset(width_time_slide, 0).perform()
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test_slide_month_pay_min(self):
        driver = self.home.driver
        # initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        annual.send_keys("240000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        down_pay = driver.find_element_by_xpath(self.home.downpay_input)
        down_pay.send_keys("20")
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(-width, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()

    def test__slide_moth_pay_max(self):
        driver = self.home.driver
        # initial values to mid range, affordable limit point<5700
        bot1 = driver.find_element_by_xpath(self.home.calculator_button)
        bot1.click()
        annual = driver.find_element_by_xpath(self.home.annual_income_input)
        annual.send_keys("240000")
        selector = Select(driver.find_element_by_xpath(self.home.state_slector))
        selector.select_by_visible_text("Alaska")
        down_pay = driver.find_element_by_xpath(self.home.downpay_input)
        down_pay.send_keys("20")
        interest = driver.find_element_by_xpath(self.home.interest_input)
        interest.send_keys("5")
        time = driver.find_element_by_xpath(self.home.time_input)
        time.send_keys("20")
        drag = ActionChains(driver)
        monthly = driver.find_element_by_css_selector(self.home.monthpay_slide_css)
        slider_left_selection_green = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        fullslider = driver.find_element_by_xpath(self.home.full_slider_track)
        fullslider = fullslider.size
        width = fullslider['width']
        width = width
        # place monthly at the min
        drag.click_and_hold(monthly).move_by_offset(width, 0).release().perform()
        drag.release(monthly)
        # get if it is affordable or not
        # get limit values
        post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = driver.find_element_by_xpath(self.home.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = driver.find_element_by_xpath(self.home.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        # compare if they are affordable
        assert slider_left_selection_green.is_displayed()
        if post1_value <= post2_value:
            affordable = True
        else:
            affordable = False
        if affordable:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#8dc63f"
            assert not alt_message.is_displayed()
            assert success_pig.is_displayed()
            assert not fail_pig.is_displayed()
        else:
            success_pig = driver.find_element_by_xpath(self.home.success_pig)
            fail_pig = driver.find_element_by_xpath(self.home.fail_pig)
            alt_message = driver.find_element_by_xpath(self.home.alt_message)
            max_amount = driver.find_element_by_xpath(self.home.max_amount)
            rgb = max_amount.value_of_css_property("color")
            color_hex = Color.from_string(rgb).hex
            assert color_hex == "#ed681f"
            assert alt_message.is_displayed()
            assert not success_pig.is_displayed()
            assert fail_pig.is_displayed()


    def tearDown(self):
        self.home.driver.close()


if __name__ == '__main__':
    unittest.main()




