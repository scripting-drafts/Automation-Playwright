from fixtures.data import rand_email
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.product_detail_page import ProductDetailPage
from pages.checkout_page import CheckoutPage
from playwright.sync_api import expect

def test_tc21_add_review_on_product(page):
    home = HomePage(page); products = ProductsPage(page); detail = ProductDetailPage(page)
    home.goto_home()
    home.open_products()
    products.open_first_product()
    detail.submit_review("Gerard", rand_email(), "Solid demo shop for automation practice.")

def test_tc23_verify_address_details_checkout_page(page):
    from fixtures.data import User, rand_name, rand_email
    from pages.auth_page import AuthPage
    from pages.signup_page import SignupPage
    from pages.cart_page import CartPage

    user = User(name=rand_name(), email=rand_email(), password="Passw0rd!")
    home = HomePage(page); auth = AuthPage(page); signup = SignupPage(page)
    products = ProductsPage(page); cart = CartPage(page); checkout = CheckoutPage(page)

    home.goto_home()
    home.nav("Signup / Login")
    auth.signup_start(user.name, user.email)
    signup.complete_signup(user.password)

    home.open_products()
    products.add_first_product_to_cart_continue()
    home.open_cart()
    cart.proceed_to_checkout()

    checkout.assert_delivery_address_contains("Carrer de Mallorca 401")
    checkout.assert_billing_address_contains("Carrer de Mallorca 401")
    auth.delete_account()

def test_tc25_verify_scroll_up_using_arrow(page):
    home = HomePage(page)
    home.goto_home()
    home.scroll_bottom()
    expect(page.locator("text=SUBSCRIPTION")).to_be_visible()
    home.click_scroll_up_arrow()
    home.assert_banner_visible()

def test_tc26_verify_scroll_up_without_arrow(page):
    home = HomePage(page)
    home.goto_home()
    home.scroll_bottom()
    expect(page.locator("text=SUBSCRIPTION")).to_be_visible()
    home.scroll_top()
    home.assert_banner_visible()
