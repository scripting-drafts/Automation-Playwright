from playwright.sync_api import expect
from .base_page import BasePage

class ProductDetailPage(BasePage):
    def assert_details_visible(self):
        expect(self.page.locator(".product-information")).to_be_visible()
        expect(self.page.locator(".product-information h2")).to_be_visible()
        expect(self.page.locator(".product-information")).to_contain_text("Category")
        expect(self.page.locator(".product-information")).to_contain_text("Availability")
        expect(self.page.locator(".product-information")).to_contain_text("Condition")
        expect(self.page.locator(".product-information")).to_contain_text("Brand")

    def set_quantity(self, qty: int):
        q = self.page.locator("#quantity")
        q.fill(str(qty))

    def add_to_cart_view_cart(self):
        self.page.locator("text=Add to cart").first.click()
        self.page.locator("text=View Cart").click()

    def submit_review(self, name: str, email: str, review: str):
        expect(self.page.locator("text=Write Your Review")).to_be_visible()
        self.page.locator("#name").fill(name)
        self.page.locator("#email").fill(email)
        self.page.locator("#review").fill(review)
        self.page.locator("#button-review").click()
        expect(self.page.locator("text=Thank you for your review.")).to_be_visible()
