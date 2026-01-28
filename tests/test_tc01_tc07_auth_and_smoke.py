from fixtures.data import User, rand_email, rand_name
from pages.home_page import HomePage
from pages.auth_page import AuthPage
from pages.signup_page import SignupPage
from pages.contact_us_page import ContactUsPage
from playwright.sync_api import expect

def test_tc01_register_user(page):
    home = HomePage(page); auth = AuthPage(page); signup = SignupPage(page)
    user = User(name=rand_name(), email=rand_email(), password="Passw0rd!")

    home.goto_home()
    home.nav("Signup / Login")
    auth.signup_start(user.name, user.email)
    signup.complete_signup(user.password)

    auth.assert_logged_in_as(user.name)
    auth.delete_account()

def test_tc03_login_user_incorrect(page):
    home = HomePage(page); auth = AuthPage(page)
    home.goto_home()
    home.nav("Signup / Login")
    auth.login("wrong@example.com", "wrongpass")
    auth.assert_login_error()

def test_tc07_verify_test_cases_page(page):
    home = HomePage(page)
    home.goto_home()
    home.open_test_cases()
    # avoid strict text selector; assert page header
    expect(page.get_by_role("heading", name="Test Cases").first).to_be_visible()

def test_tc06_contact_us_form(page, tmp_path):
    home = HomePage(page); contact = ContactUsPage(page)
    home.goto_home()
    home.open_contact_us()
    contact.assert_loaded()

    f = tmp_path / "upload.txt"
    f.write_text("upload from playwright")

    contact.submit_form(
        name="Gerard",
        email=rand_email(),
        subject="Automation question",
        message="Hello, testing the contact form.",
        upload_path=str(f),
    )
    home.nav("Home")
    home.assert_loaded()
