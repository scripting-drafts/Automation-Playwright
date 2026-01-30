import re
from playwright.sync_api import expect
from .base_page import BasePage

class ContactUsPage(BasePage):
    def assert_loaded(self):
        expect(self.page.locator("text=GET IN TOUCH")).to_be_visible()

    def submit_form(self, name: str, email: str, subject: str, message: str, upload_path: str):
        self.page.locator('input[data-qa="name"]').fill(name)
        self.page.locator('input[data-qa="email"]').fill(email)
        self.page.locator('input[data-qa="subject"]').fill(subject)
        self.page.locator('textarea[data-qa="message"]').fill(message)
        self.page.set_input_files('input[name="upload_file"]', upload_path)

        dialog_text = {}

        def handle_dialog(d):
            dialog_text["message"] = d.message
            d.accept()

        self.page.once("dialog", handle_dialog)

        self.page.locator('input[data-qa="submit-button"]').click()

