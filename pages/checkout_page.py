import re
from playwright.sync_api import expect, TimeoutError as PlaywrightTimeoutError
from .base_page import BasePage

class CheckoutPage(BasePage):
    def assert_address_and_review_visible(self):
        expect(self.page.locator("text=Address Details")).to_be_visible()
        expect(self.page.locator("text=Review Your Order")).to_be_visible()

    def place_order_and_pay(self):
        self.page.locator("textarea[name='message']").fill("Please deliver ASAP.")
        self.page.locator("text=Place Order").click()

        try:
            self.page.locator('input[data-qa="name-on-card"]').fill("QA Engineer")
        except PlaywrightTimeoutError:
            if "google_vignette" in self.page.url:
                try:
                    self.page.go_back(wait_until="domcontentloaded")
                except Exception:
                    pass
                self.page.locator("text=Place Order").click()
                self.page.locator('input[data-qa="name-on-card"]').fill("QA Engineer")
            else:
                raise
        self.page.locator('input[data-qa="card-number"]').fill("4111111111111111")
        self.page.locator('input[data-qa="cvc"]').fill("123")
        self.page.locator('input[data-qa="expiry-month"]').fill("12")
        self.page.locator('input[data-qa="expiry-year"]').fill("2030")
        self.page.locator('button[data-qa="pay-button"]').click()

        expect(self.page.locator("text=Your order has been placed successfully!"))

    def download_invoice(self):
        with self.page.expect_download() as d:
            self.page.locator("text=Download Invoice").click()
        download = d.value
        assert download.suggested_filename.lower().endswith((".txt", ".pdf")), download.suggested_filename

    def continue_after_order(self):
        self.page.locator("text=Continue").click()

    def assert_delivery_address_contains(self, text: str):
        expect(self.page.locator("#address_delivery")).to_contain_text(text)

    def assert_billing_address_contains(self, text: str):
        expect(self.page.locator("#address_invoice")).to_contain_text(text)
