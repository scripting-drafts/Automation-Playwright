import os
import pytest
import re
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BASE_URL = "https://www.automationexercise.com"

SSL_ERROR_PATTERNS = re.compile(
    r"(ERR_SSL|SSL_HANDSHAKE|CERT_|certificate)",
    re.IGNORECASE,
)

CONSENT_INIT_SCRIPT = r"""
(() => {
  const kill = () => {
    const nodes = document.querySelectorAll(
      '#fc-consent-root, .fc-consent-root, .fc-dialog-overlay, .fc-overlay, .fc-consent-dialog, .fc-dialog'
    );
    for (const el of nodes) {
      el.style.setProperty('pointer-events', 'none', 'important');
      el.style.setProperty('display', 'none', 'important');
      el.style.setProperty('visibility', 'hidden', 'important');
      el.style.setProperty('opacity', '0', 'important');
      el.remove();
    }
    document.documentElement.style.overflow = 'auto';
    document.body.style.overflow = 'auto';
  };

  kill();

  // Re-injection safe: mutation observer
  const obs = new MutationObserver(() => kill());
  obs.observe(document.documentElement, { childList: true, subtree: true });

  // Some consent managers inject on interaction
  window.addEventListener('load', kill, { once: false });
  window.addEventListener('scroll', kill, { passive: true });
  window.addEventListener('pointerdown', kill, { passive: true });
})();
"""

@pytest.fixture(scope="session")
def browser():
  headless = os.getenv("HEADLESS", "1") == "1"
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=headless)
    context = browser.new_context()

    page = context.new_page()
    page.goto("https://www.automationexercise.com", wait_until="domcontentloaded")

    try:
      page.locator(
        "button:has-text('Consent'), button:has-text('Accept')"
      ).first.click(timeout=3000)
    except PlaywrightTimeoutError:
      pass

    context.storage_state(path="auth_state.json")
    context.close()
    yield browser

    browser.close()

@pytest.fixture()
def page(browser):
  context = browser.new_context(
    accept_downloads=True,
    bypass_csp=True,
    viewport={"width": 1280, "height": 720},
    ignore_https_errors=True,
    storage_state="auth_state.json"
  )
  context.add_init_script(CONSENT_INIT_SCRIPT)

  p = context.new_page()
  p.set_default_timeout(15000)
  p.set_default_navigation_timeout(30000)

  def _consent_guard():
    try:
      p.evaluate("""() => {
        const nodes = document.querySelectorAll(
          '#fc-consent-root, .fc-consent-root, .fc-dialog-overlay, .fc-overlay, .fc-consent-dialog, .fc-dialog'
        );
        nodes.forEach(el => { el.remove(); });
        document.documentElement.style.overflow = 'auto';
        document.body.style.overflow = 'auto';
      }""")
    except Exception:
      pass

  p.on("domcontentloaded", lambda: _consent_guard())
  p.on("load", lambda: _consent_guard())

  try:
        p.locator(
            "button:has-text('Consent'), button:has-text('Accept')"
        ).first.click(timeout=3000)
  except:
      pass

  yield p
  context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    try:
        yield
    except Exception as e:
        msg = str(e)
        if SSL_ERROR_PATTERNS.search(msg):
            pytest.skip(f"Infrastructure SSL failure: {msg}")
        raise