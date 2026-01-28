from playwright.sync_api import expect
from .base_page import BasePage

class SignupPage(BasePage):
    def assert_account_info(self):
        expect(self.page.locator("text=ENTER ACCOUNT INFORMATION")).to_be_visible()

    def complete_signup(self, password: str):
        self.assert_account_info()

        self.page.locator('input#id_gender1').check()
        self.page.locator('input[data-qa="password"]').fill(password)

        self.page.locator('select[data-qa="days"]').select_option("10")
        self.page.locator('select[data-qa="months"]').select_option("1")
        self.page.locator('select[data-qa="years"]').select_option("1990")

        self.page.locator('input#newsletter').check()
        self.page.locator('input#optin').check()

        self.page.locator('input[data-qa="first_name"]').fill("Gerard")
        self.page.locator('input[data-qa="last_name"]').fill("Sala")
        self.page.locator('input[data-qa="company"]').fill("QA Labs")
        self.page.locator('input[data-qa="address"]').fill("Carrer de Mallorca 401")
        self.page.locator('input[data-qa="address2"]').fill("Sagrada Familia")
        self.page.locator('select[data-qa="country"]').select_option("Canada")
        self.page.locator('input[data-qa="state"]').fill("BC")
        self.page.locator('input[data-qa="city"]').fill("Vancouver")
        self.page.locator('input[data-qa="zipcode"]').fill("V6B1A1")
        self.page.locator('input[data-qa="mobile_number"]').fill("600123123")

        btn = self.page.locator('button[data-qa="create-account"]')
        self.safe_click(btn)
        expect(self.page.locator("text=ACCOUNT CREATED!")).to_be_visible()
        self.page.get_by_role("link", name="Continue").click()
