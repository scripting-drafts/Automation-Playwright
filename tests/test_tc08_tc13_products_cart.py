from fixtures.data import rand_email
from pages.home_page import HomePage
from pages.products_page import ProductsPage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage

def test_tc08_verify_all_products_and_detail(page):
    home = HomePage(page); products = ProductsPage(page); detail = ProductDetailPage(page)
    home.goto_home()
    home.open_products()
    products.assert_loaded()
    products.open_first_product()
    detail.assert_details_visible()

def test_tc09_search_product(page):
    home = HomePage(page); products = ProductsPage(page)
    home.goto_home()
    home.open_products()
    products.assert_loaded()
    products.search("top")

def test_tc10_verify_subscription_home(page):
    home = HomePage(page)
    home.goto_home()
    home.subscribe(rand_email())

def test_tc11_verify_subscription_cart(page):
    home = HomePage(page)
    home.goto_home()
    home.open_cart()
    home.subscribe(rand_email())

def test_tc12_add_products_in_cart(page):
    home = HomePage(page); products = ProductsPage(page); cart = CartPage(page)
    home.goto_home()
    home.open_products()
    products.assert_loaded()
    products.add_first_two_products_to_cart_view_cart()
    cart.assert_loaded()
    cart.assert_items_count(2)

def test_tc13_verify_product_quantity_in_cart(page):
    home = HomePage(page); products = ProductsPage(page); detail = ProductDetailPage(page); cart = CartPage(page)
    home.goto_home()
    home.open_products()
    products.open_first_product()
    detail.set_quantity(4)
    detail.add_to_cart_view_cart()
    cart.assert_qty_for_first_item(4)
