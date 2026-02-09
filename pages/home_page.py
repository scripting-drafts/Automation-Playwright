from playwright.sync_api import expect
from .base_page import BasePage

class HomePage(BasePage):
    def assert_loaded(self):
        expect(self.page.locator("a[href='/login']")).to_be_visible()

    def open_test_cases(self):
        self.nav("Test Cases")

    def open_products(self):
        self.nav("Products")

    def open_cart(self):
        self.nav("Cart")

    def open_contact_us(self):
        self.nav("Contact us")

    def subscribe(self, email: str):
        self.scroll_bottom()
        expect(self.page.locator("text=SUBSCRIPTION").first).to_be_visible()
        self.page.locator("#susbscribe_email").fill(email)
        self.page.locator("#subscribe").click()
        expect(self.page.locator("text=You have been successfully subscribed!").first).to_be_visible()

    def click_scroll_up_arrow(self):
        self.page.locator("#scrollUp").click()

    def assert_banner_visible(self):
        expect(self.page.get_by_role("heading", name="Full-Fledged practice website for Automation Engineers").first).to_be_visible()
