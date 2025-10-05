# whatsapp_async_session.py
import os
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PWTimeoutError

PROFILE_DIR = str(Path.home() / "whatsapp_async_profile")
HEADLESS = False


async def get_logged_in_page():
    """Launch browser with persistent session (asks QR only once)."""
    os.makedirs(PROFILE_DIR, exist_ok=True)
    print(f"🧩 Using persistent profile: {PROFILE_DIR}")

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=HEADLESS,
        args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
    )
    page = await browser.new_page()
    await page.goto("https://web.whatsapp.com")

    print("[INFO] Waiting for WhatsApp login (scan QR if needed)...")
    try:
        await page.wait_for_selector('div[aria-label="Chat list"]', timeout=120_000)
        print("✅ Login successful.")
    except PWTimeoutError:
        print("⚠️ Timeout waiting for WhatsApp chat list.")
        await browser.close()
        await playwright.stop()
        return None, None, None

    return playwright, browser, page
