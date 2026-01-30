import re
from playwright.sync_api import expect
from .base_page import BasePage

class AuthPage(BasePage):
    def assert_login_visible(self):
        expect(self.page.locator("text=Login to your account")).to_be_visible()

    def assert_signup_visible(self):
        expect(self.page.locator("text=New User Signup!")).to_be_visible()

    def login(self, email: str, password: str):
        self.assert_login_visible()
        self.page.locator('input[data-qa="login-email"]').fill(email)
        self.page.locator('input[data-qa="login-password"]').fill(password)
        self.page.locator('button[data-qa="login-button"]').click()

    def signup_start(self, name: str, email: str):
        self.assert_signup_visible()
        self.page.locator('input[data-qa="signup-name"]').fill(name)
        self.page.locator('input[data-qa="signup-email"]').fill(email)
        self.page.locator('button[data-qa="signup-button"]').click()

    def assert_login_error(self):
        expect(self.page).to_have_url(re.compile(r"/login"), timeout=15000)
        expect(self.page.get_by_text(re.compile(r"email or password is incorrect", re.I))).to_be_visible()

    def assert_signup_existing_email_error(self):
        expect(self.page.locator("text=Email Address already exist!")).to_be_visible()

    def assert_logged_in_as(self, name: str):
        expect(self.page.locator("text=Logged in as")).to_be_visible()
        expect(self.page.locator(f"text={name}")).to_be_visible()

    def logout(self):
        self.nav("Logout")
        self.assert_login_visible()

    def delete_account(self):
        self.nav("Delete Account")
        expect(self.page.get_by_text(re.compile(r"ACCOUNT\s+DELETED", re.I))).to_be_visible()
        self.page.get_by_role("link", name=re.compile(r"Continue", re.I)).first.click()
