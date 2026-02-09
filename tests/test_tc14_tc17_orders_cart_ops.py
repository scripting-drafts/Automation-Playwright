from fixtures.data import User, rand_email, rand_name
from pages.home_page import HomePage
from pages.auth_page import AuthPage
from pages.signup_page import SignupPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def _signup_flow(page, user):
    home = HomePage(page); auth = AuthPage(page); signup = SignupPage(page)
    home.goto_home()
    home.nav("Signup / Login")
    auth.signup_start(user.name, user.email)
    signup.complete_signup(user.password)
    auth.assert_logged_in_as(user.name)

def test_tc14_place_order_register_while_checkout(page):
    user = User(name=rand_name(), email=rand_email(), password="Passw0rd!")
    home = HomePage(page); products = ProductsPage(page); cart = CartPage(page); checkout = CheckoutPage(page)
    auth = AuthPage(page); signup = SignupPage(page)

    home.goto_home()
    home.open_products()
    products.add_first_product_to_cart_continue()
    home.open_cart()
    cart.proceed_to_checkout()

    cart.click_login_to_checkout()
    auth.signup_start(user.name, user.email)
    signup.complete_signup(user.password)
    auth.assert_logged_in_as(user.name)

    home.open_cart()
    cart.proceed_to_checkout()
    checkout.assert_address_and_review_visible()
    checkout.place_order_and_pay()
    auth.delete_account()

def test_tc15_place_order_register_before_checkout(page):
    user = User(name=rand_name(), email=rand_email(), password="Passw0rd!")
    _signup_flow(page, user)

    home = HomePage(page); products = ProductsPage(page); cart = CartPage(page); checkout = CheckoutPage(page); auth = AuthPage(page)
    home.open_products()
    products.add_first_product_to_cart_continue()
    home.open_cart()
    cart.proceed_to_checkout()
    checkout.assert_address_and_review_visible()
    checkout.place_order_and_pay()
    auth.delete_account()

def test_tc16_download_invoice_after_purchase(page):
    user = User(name=rand_name(), email=rand_email(), password="Passw0rd!")
    home = HomePage(page); products = ProductsPage(page); cart = CartPage(page); checkout = CheckoutPage(page)
    auth = AuthPage(page); signup = SignupPage(page)

    home.goto_home()
    home.open_products()
    products.add_first_product_to_cart_continue()
    home.open_cart()
    cart.proceed_to_checkout()

    cart.click_login_to_checkout()
    auth.signup_start(user.name, user.email)
    signup.complete_signup(user.password)
    auth.assert_logged_in_as(user.name)

    home.open_cart()
    cart.proceed_to_checkout()
    checkout.place_order_and_pay()
    checkout.download_invoice()
    checkout.continue_after_order()
    auth.delete_account()

def test_tc17_remove_products_from_cart(page):
    home = HomePage(page); products = ProductsPage(page); cart = CartPage(page)
    home.goto_home()
    home.open_products()
    products.add_first_product_to_cart_continue()
    home.open_cart()
    cart.assert_loaded()
    cart.remove_first_item()
    cart.assert_items_count(0)


