from playwright.sync_api import expect
from .base_page import BasePage

class ProductsPage(BasePage):
    def _close_cart_modal(self, *, view_cart: bool = False):
        """After 'Add to cart' a modal appears. Close it deterministically.

        The cookie/consent overlay occasionally re-appears and can intercept clicks,
        so we target the modal content and use force as a last resort.
        """
        modal = self.page.locator(".modal-content").first
        expect(modal).to_be_visible()

        if view_cart:
            btn = modal.get_by_role("link", name="View Cart")
        else:
            btn = modal.get_by_role("button", name="Continue Shopping")

        expect(btn).to_be_visible()
        btn.click(force=True)

    def assert_loaded(self):
        expect(self.page.locator("text=All Products")).to_be_visible()
        expect(self.page.locator(".features_items")).to_be_visible()

    def search(self, term: str):
        self.page.locator("#search_product").fill(term)
        self.page.locator("#submit_search").click()
        expect(self.page.locator("text=SEARCHED PRODUCTS")).to_be_visible()

    def open_first_product(self):
        self.page.locator("text=View Product").first.click()

    def add_first_product_to_cart_continue(self):
        first = self.page.locator(".product-image-wrapper").first
        first.hover()
        first.locator("text=Add to cart").first.click()
        self._close_cart_modal(view_cart=False)
        self._continue_shopping()

    def add_first_two_products_to_cart_view_cart(self):
        first = self.page.locator(".product-image-wrapper").nth(0)
        first.hover()
        first.locator("text=Add to cart").first.click()
        self._close_cart_modal(view_cart=False)

        second = self.page.locator(".product-image-wrapper").nth(1)
        second.hover()
        second.locator("text=Add to cart").first.click()
        self._close_cart_modal(view_cart=True)

    def _continue_shopping(self):
        try:
            expect(self.page.locator("text=Your product has been added to cart.")).to_be_visible(timeout=2000)
            self.page.locator("text=Continue Shopping").first.click()
        except:
            pass