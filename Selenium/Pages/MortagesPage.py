from Pages import aPage


class MortgagesPage(aPage):
    def start(self):
        self.url = "finance/finance__companies.htm"
        self.open_page(self.url, 'Max')
        # Assert Title of the Login Page and Login
        self.assertIn("Best Mortgage Lenders and Refinancing Companies | ConsumerAffairs", self.driver.title)
        self.howto_buton = "//nav[@id='aside-nav']/a[@href='#how-to-apply-for-a-mortgage']"
        self.calculator_button = "/html//div[@id='how-to-apply-for-a-mortgage-content']//a[@href='https://www.consumeraffairs.com/finance/how-much-house-can-i-afford.html#']"
