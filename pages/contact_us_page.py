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

        self.page.on("dialog", lambda d: d.accept())
        self.page.locator('input[data-qa="submit-button"]').click()

        # Success message is shown in an alert box (wording can vary slightly).
        success = self.page.locator(".status.alert-success, .alert-success").first
        expect(success).to_be_visible()
        expect(success).to_contain_text(re.compile(r"success", re.I))
