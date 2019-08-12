"""
test for navigation to the Mortage section
"""
import unittest
from selenium import webdriver as wd
from Pages.aPage import Page
from Pages.HomePage import HomePage
from Pages.BuyersGuides import BuyersGuide
from Pages.MortagesPage import MortgagesPage
from Pages.MortageCalculator import MortgageCalculator
from selenium.webdriver.common.keys import Keys
from utilSetup.LinkTest import TestLinks
import HtmlTestRunner

#Test Case described on Section 2, related to excell file sheet: TestScenarioMortage
class Navigate_to_mortage(unittest.TestCase):

    def setUp(self):
        driver = wd.Chrome(executable_path="../Drivers/chromedriver.exe")
        self.the_page = Page(driver, "")

    def test_1366x768(self):
        #navigates and check for links
        self.the_page.open_page("1366x768")
        self.assertIn(HomePage.title, self.the_page.driver.title)
        self.the_page.click_elm(HomePage.resources_button)
        self.assertIn(BuyersGuide.title, self.the_page.driver.title)
        self.the_page.click_elm(BuyersGuide.finance_buton)
        self.the_page.click_elm(BuyersGuide.mortage_button)
        self.assertIn(MortgagesPage.title, self.the_page.driver.title)
        self.the_page.find_by_xpath(MortgagesPage.howto_buton).send_keys(Keys.ENTER)
        self.the_page.find_by_xpath(MortgagesPage.calculator_button).send_keys(Keys.ENTER)
        self.assertIn(MortgageCalculator.title, self.the_page.driver.title)
        TestLinks.check_Links(self,self.the_page.driver)

    def test_1920x1080(self):
        #navigates and check for links
        self.the_page.open_page("1920x1080")
        self.assertIn(HomePage.title, self.the_page.driver.title)
        self.the_page.click_elm(HomePage.resources_button)
        self.assertIn(BuyersGuide.title, self.the_page.driver.title)
        self.the_page.click_elm(BuyersGuide.finance_buton)
        self.the_page.click_elm(BuyersGuide.mortage_button)
        self.assertIn(MortgagesPage.title, self.the_page.driver.title)
        self.the_page.find_by_xpath(MortgagesPage.howto_buton).send_keys(Keys.ENTER)
        self.the_page.find_by_xpath(MortgagesPage.calculator_button).send_keys(Keys.ENTER)
        self.assertIn(MortgageCalculator.title, self.the_page.driver.title)
        TestLinks.check_Links(self,self.the_page.driver)

    def test_1440x900(self):
        #navigates and check for links
        self.the_page.open_page("1440x900")
        self.assertIn(HomePage.title, self.the_page.driver.title)
        self.the_page.click_elm(HomePage.resources_button)
        self.assertIn(BuyersGuide.title, self.the_page.driver.title)
        self.the_page.click_elm(BuyersGuide.finance_buton)
        self.the_page.click_elm(BuyersGuide.mortage_button)
        self.assertIn(MortgagesPage.title, self.the_page.driver.title)
        self.the_page.find_by_xpath(MortgagesPage.howto_buton).send_keys(Keys.ENTER)
        self.the_page.find_by_xpath(MortgagesPage.calculator_button).send_keys(Keys.ENTER)
        self.assertIn(MortgageCalculator.title, self.the_page.driver.title)
        TestLinks.check_Links(self,self.the_page.driver)

    def test_1280x720(self):
        #navigates and check for links
        self.the_page.open_page("1280x720")
        self.assertIn(HomePage.title, self.the_page.driver.title)
        self.the_page.click_elm(HomePage.resources_button)
        self.assertIn(BuyersGuide.title, self.the_page.driver.title)
        self.the_page.click_elm(BuyersGuide.finance_buton)
        self.the_page.click_elm(BuyersGuide.mortage_button)
        self.assertIn(MortgagesPage.title, self.the_page.driver.title)
        self.the_page.find_by_xpath(MortgagesPage.howto_buton).send_keys(Keys.ENTER)
        self.the_page.find_by_xpath(MortgagesPage.calculator_button).send_keys(Keys.ENTER)
        self.assertIn(MortgageCalculator.title, self.the_page.driver.title)
        TestLinks.check_Links(self,self.the_page.driver)

    def tearDown(self):
        self.the_page.driver.close()

#this is the class to run.
class MyTestSuite(unittest.TestCase):

    def test_suit_excecuter(self):
        smoke_test = unittest.TestSuite()
        smoke_test.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(Navigate_to_mortage),
        ])
        runner1 = HtmlTestRunner.HTMLTestRunner(output="../Reports")
        runner1.run(smoke_test)










