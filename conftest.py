import os
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.automationexercise.com"

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
    b = p.chromium.launch(headless=headless)
    yield b
    b.close()

@pytest.fixture()
def page(browser):
  context = browser.new_context(
    accept_downloads=True,
    bypass_csp=True,
    viewport={"width": 1280, "height": 720},
  )
  context.add_init_script(CONSENT_INIT_SCRIPT)

  p = context.new_page()
  p.set_default_timeout(15000)
  p.set_default_navigation_timeout(30000)

  def _consent_guard():
    # Extra safety for pages where overlay appears “after some navigation”
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

  # Run guard on every load milestone
  p.on("domcontentloaded", lambda: _consent_guard())
  p.on("load", lambda: _consent_guard())

  yield p
  context.close()
