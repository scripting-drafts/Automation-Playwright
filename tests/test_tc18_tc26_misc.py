from fixtures.data import User, rand_email, rand_name
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.product_detail_page import ProductDetailPage
from pages.checkout_page import CheckoutPage
from playwright.sync_api import expect

def test_tc18_view_category_products(page):
    home = HomePage(page); products = ProductsPage(page)
    home.goto_home()
    home.open_products()

    page.locator("#accordian .panel-heading a").first.click()
    page.locator("#accordian a[href*='/category_products/1']").first.click()
    expect(page.locator(".features_items")).to_be_visible()

def test_tc19_view_and_cart_brand_products(page):
    home = HomePage(page); products = ProductsPage(page)
    home.goto_home()
    home.open_products()

    page.locator(".brands_products a[href*='/brand_products/']").first.click()
    expect(page.locator(".features_items")).to_be_visible()

    first_brand_product = page.locator(".features_items .product-image-wrapper").first
    first_brand_product.hover()
    first_brand_product.locator("text=Add to cart").first.click()
    modal = page.locator(".modal-content").first
    expect(modal).to_be_visible()
    modal.get_by_role("button", name="Continue Shopping").click(force=True)

def test_tc20_search_products_and_verify_cart_after_login(page):
    home = HomePage(page); products = ProductsPage(page)
    user = User(name=rand_name(), email=rand_email(), password="Passw0rd!")

    home.goto_home()
    home.open_products()
    products.search("dress")
    first_result = page.locator(".features_items .product-image-wrapper").first
    first_result.hover()
    first_result.locator("text=Add to cart").first.click()
    modal = page.locator(".modal-content").first
    expect(modal).to_be_visible()
    modal.get_by_role("link", name="View Cart").click(force=True)

    from pages.cart_page import CartPage
    from pages.auth_page import AuthPage
    from pages.signup_page import SignupPage

    cart = CartPage(page); auth = AuthPage(page); signup = SignupPage(page)
    cart.assert_loaded()
    home.nav("Signup / Login")

    auth.signup_start(user.name, user.email)
    signup.complete_signup(user.password)
    auth.assert_logged_in_as(user.name)

    home.open_cart()
    cart.assert_loaded()
    cart.assert_items_count(1)

def test_tc21_add_review_on_product(page):
    home = HomePage(page); products = ProductsPage(page); detail = ProductDetailPage(page)
    home.goto_home()
    home.open_products()
    products.open_first_product()
    detail.submit_review("Gerard", rand_email(), "Solid demo shop for automation practice.")

def test_tc22_add_to_cart_from_recommended_items(page):
    from pages.cart_page import CartPage

    home = HomePage(page)
    cart = CartPage(page)

    home.goto_home()
    home.scroll_bottom()
    expect(page.locator(".recommended_items")).to_be_visible()

    first_recommended = page.locator(".recommended_items .product-image-wrapper").first
    first_recommended.hover()
    first_recommended.locator("text=Add to cart").first.click()

    modal = page.locator(".modal-content").first
    expect(modal).to_be_visible()
    modal.get_by_role("link", name="View Cart").click(force=True)

    cart.assert_loaded()
    cart.assert_items_count(1)

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

def test_tc24_download_invoice_after_purchase_order(page):
    home = HomePage(page); products = ProductsPage(page); checkout = CheckoutPage(page)
    from pages.cart_page import CartPage
    from pages.auth_page import AuthPage
    from pages.signup_page import SignupPage

    user = User(name=rand_name(), email=rand_email(), password="Passw0rd!")
    cart = CartPage(page); auth = AuthPage(page); signup = SignupPage(page)

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
