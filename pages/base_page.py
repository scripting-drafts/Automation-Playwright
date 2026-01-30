from playwright.sync_api import expect

BASE_URL = "https://www.automationexercise.com"


class BasePage:
    """Shared helpers.

    NOTE: We intentionally avoid get_by_role(..., name=re.compile(...)) for navigation on this site.
    Some Playwright builds serialize regex-containing accessible names into an internal selector form
    that breaks parsing when the text contains "/" or escape sequences (Windows showed this).
    We instead navigate via stable hrefs in the top navbar.
    """

    NAV_HREF = {
        "Home": "/",
        "Products": "/products",
        "Cart": "/view_cart",
        "Signup / Login": "/login",
        "Test Cases": "/test_cases",
        "Contact us": "/contact_us",
        "Logout": "/logout",
        "Delete Account": "/delete_account",
    }

    def __init__(self, page):
        self.page = page

    def goto_home(self):
        self.page.goto(BASE_URL, wait_until="domcontentloaded")
        expect(self.page.locator("a[href='/login']")).to_be_visible()

    def nav(self, link_text: str):
        href = self.NAV_HREF.get(link_text)
        if href:
            self.safe_click(self.page.locator(f"header a[href='{href}']").first)
            return
        
        self.safe_click(self.page.locator("header a").filter(has_text=link_text).first)

    def scroll_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_top(self):
        self.page.evaluate("window.scrollTo(0, 0)")

    def kill_consent_if_present(self):
        self.page.evaluate("""
        () => {
        const nodes = document.querySelectorAll(
            '#fc-consent-root, .fc-consent-root, .fc-dialog-overlay, .fc-overlay'
        );
        nodes.forEach(el => {
            el.style.setProperty('pointer-events','none','important');
            el.style.setProperty('display','none','important');
            el.remove();
        });
        document.documentElement.style.overflow = 'auto';
        document.body.style.overflow = 'auto';
        }
        """)

    def safe_click(self, locator):
        self.kill_consent_if_present()
        try:
            locator.click(timeout=5000)
        except Exception:
            self.kill_consent_if_present()
            locator.click(force=True, timeout=5000)