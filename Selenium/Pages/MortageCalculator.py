from Pages.aPage import Page
import re


class MortgageCalculator(Page):
    calculator_button = "//section[@id='introduction']//a[@href='https://www.consumeraffairs.com/finance/how-much-house-can-i-afford.html#calculator']"
    annual_income_input = "/html//section[@id='calculator']/div/div//input[@name='household_income']"
    interest_input = "/html//section[@id='calculator']/div/div//input[@name='interest_rate']"
    downpay_input = "/html//section[@id='calculator']/div/div//input[@name='down_payment']"
    time_input = "/html//section[@id='calculator']/div/div//input[@name='mortgage_term']"
    state_slector = "/html//section[@id='calculator']/div/div//select[@name='state_value']"
    annual_income_slide = "/html//section[@id='calculator']/div/div/div[3]/div[1]/div[@class='slider_inside']/div[@class='slider slider-horizontal']/div[5]"
    full_annual_income_slide = "/html//section[@id='calculator']/div/div/div[3]/div[1]/div[@class='slider_inside']/div[@class='slider slider-horizontal']"
    interest_slide = "/html//section[@id='calculator']/div/div/div[3]/div[2]/div[@class='slider_inside']/div[@class='slider slider-horizontal']/div[5]"
    downpay_slide = "/html//section[@id='calculator']/div/div/div[3]/div[3]/div[@class='slider_inside']/div[@class='slider slider-horizontal']/div[5]"
    time_slide = "/html//section[@id='calculator']/div/div/div[3]/div[4]/div[@class='slider_inside']/div[@class='slider slider-horizontal']/div[5]"
    monthpay_slide = "/html//section[@id='calculator']/div//div[@class='m_s_g']/div[@class='slider_inside']/div[@class='slider slider-horizontal']/div[5]"
    slider_left_selection_green = "/html//section[@id='calculator']/div//div[@class='m_s_g']/div[@class='slider_inside']/div[@class='slider slider-horizontal']//div[@class='slider-rangeHighlight slider-selection']"
    slider_left_selection_orange = "/html//section[@id='calculator']/div//div[@class='m_s_g']/div[@class='slider_inside']/div[@class='slider slider-horizontal']//div[@class='slider-rangeHighlight slider-selection']"
    slider_right_selection = "/html//section[@id='calculator']/div//div[@class='m_s_g']/div[@class='slider_inside']/div[@class='slider slider-horizontal']//div[@class='slider-rangeHighlight slider-selection']"
    monthpay_slide_css = ".m_s_g .slider-horizontal [role='slider']:nth-of-type(5)"
    fail_pig = "/html//section[@id='calculator']/div/div/div[4]/div[@class='fail']"
    success_pig = "/html//section[@id='calculator']/div/div/div[4]/div[@class='success']"
    alt_message = "/html//section[@id='calculator']/div//div[@class='fail_visibility']/span"
    max_amount = "/html//section[@id='calculator']/div/div//span[@class='count_val_afford']"
    full_slider_track = "/html//section[@id='calculator']/div//div[@class='m_s_g']/div[@class='slider_inside']/div[@class='slider slider-horizontal']"
    interest_slide = "/html//section[@id='calculator']/div/div/div[3]/div[2]/div[@class='slider_inside']/div[@class='slider slider-horizontal']/div[5]"
    interest_slide_track = "/html//section[@id='calculator']/div/div/div[3]/div[2]/div[@class='slider_inside']/div[@class='slider slider-horizontal']"
    down_pay_slide = "/html//section[@id='calculator']/div/div/div[3]/div[3]/div[@class='slider_inside']/div[@class='slider slider-horizontal']/div[5]"
    down_pay_slide_track = "/html//section[@id='calculator']/div/div/div[3]/div[3]/div[@class='slider_inside']/div[@class='slider slider-horizontal']"
    time_slide = "/html//section[@id='calculator']/div/div/div[3]/div[4]/div[@class='slider_inside']/div[@class='slider slider-horizontal']/div[5]"
    time_slide_track = "/html//section[@id='calculator']/div/div/div[3]/div[4]/div[@class='slider_inside']/div[@class='slider slider-horizontal']"
    title = "Mortgage Calculator | ConsumerAffairs"

    def __init__(self, selen_dirver, added_url):
        super().__init__(selen_dirver, added_url)
        # Assert Title of the Login Page and Login
        self.driver.get(self.main_url)
        assert self.title == self.driver.title




    def set_mid_values(self):
        #sets all the values to the standar mid ranges for testing
        self.driver.find_element_by_xpath(self.calculator_button).click()
        self.driver.find_element_by_xpath(self.annual_income_input).send_keys("240000")
        self.driver.find_element_by_xpath(self.interest_input).send_keys("5")
        self.driver.find_element_by_xpath(self.downpay_input).send_keys("135000")
        self.driver.find_element_by_xpath(self.time_input).send_keys("20")
        self.driver.find_element_by_xpath(self.monthpay_slide).click()

    def move_slide(self, which_to, amount):
        self.drag_something(which_to, amount)

    def is_affordable(self):
        post1 = self.find_by_xpath(self.monthpay_slide)
        post1_value = post1.get_attribute("style")
        post1_value = re.findall("\d+.\d+", post1_value)
        if not post1_value:
            post1 = self.find_by_xpath(self.monthpay_slide)
            post1_value = post1.get_attribute("style")
            post1_value = re.findall("\d+", post1_value)
        post1_value = float(post1_value[0])
        post2 = self.find_by_xpath(self.slider_left_selection_green)
        post2_value = post2.get_attribute("style")
        post2_value = re.split(r":", post2_value)
        post2_value = post2_value[2]
        post2_value = re.findall("\d+.\d+", post2_value)
        if not post2_value:
            post2 = self.find_by_xpath(self.slider_left_selection_green)
            post2_value = post2.get_attribute("style")
            post2_value = re.split(r":", post2_value)
            post2_value = post2_value[2]
            post2_value = re.findall("\d+", post2_value)
        post2_value = float(post2_value[0])
        if post1_value <= post2_value:
            return True
        else:
            return False



