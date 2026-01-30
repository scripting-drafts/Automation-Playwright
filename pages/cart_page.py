from playwright.sync_api import expect

from conftest import page
from .base_page import BasePage

class CartPage(BasePage):
    def assert_loaded(self):
        expect(self.page.locator("text=Shopping Cart")).to_be_visible()

    def proceed_to_checkout(self):
        self.page.locator("text=Proceed To Checkout").click()

    def remove_first_item(self):
        self.page.locator(".cart_quantity_delete").first.click()

    def assert_items_count(self, count: int):
        expect(self.page.locator("tbody tr")).to_have_count(count)

    def assert_qty_for_first_item(self, qty: int):
        expect(self.page.locator("tbody tr td.cart_quantity button")).to_have_text(str(qty))

    def click_login_to_checkout(self):
        login_link = ".modal-body > p:nth-child(2) > a:nth-child(1) > u:nth-child(1)"
        self.page.locator(login_link).click()