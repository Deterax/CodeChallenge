from Pages import aPage


class BuyersGuide(aPage):
    def start(self):
        self.url = "resources/"
        self.open_page(self.url, 'Max')
        # Assert Title of the Login Page and Login
        self.assertIn("Resources by Topic - ConsumerAffairs", self.driver.title)
        self.finance_buton = "/html//main[@id='wrpr']//div[@class='h-hd-main']/div[2]//div[@class='card-grd card-grd--mb-no-pad']/div[8]/a[@href='#']"
        self.mortage_button = "/html//main[@id='wrpr']//div[@class='h-hd-main']/div[2]/div[2]//a[@href='https://www.consumeraffairs.com/finance/finance__companies.htm']"
