from Pages import aPage


class HomePage (aPage):
    def __init__(self, selen_dirver):
        super().__init__(selen_dirver, "")
        # Assert Title of the Login Page and Login
        self.driver.get(self.main_url)
        self.open_page(self.url, 'Max')
        # Assert Title of the Login Page and Login
        self.assertIn("ConsumerAffairs.com: Research. Review. Resolve.", self.driver.title)
        self.resources_button ="//header[@id='ca-hdr']//nav[@class='ca-hdr__main-nav ca-hdr__mb-menu']/ul[@role='menu']/li[1]/a[@role='menuitem']"
