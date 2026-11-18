# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

PROFILE_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\chrome_aff_profile"
target_url = "https://affiliate.shopee.vn/offer/product_offer/24964977977"

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        PROFILE_DIR,
        channel="chrome",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized"
        ],
        ignore_default_args=["--enable-automation"]
    )
    page = context.pages[0] if context.pages else context.new_page()
    
    # Bypass navigator.webdriver
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)
    
    page.goto(target_url, wait_until="domcontentloaded")
    time.sleep(5)
    
    screenshot_path = r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\debug_page_stealth.png"
    page.screenshot(path=screenshot_path)
    print("Screenshot saved to debug_page_stealth.png")
    
    buttons = page.locator("button").all()
    print("Buttons count:", len(buttons))
    for i, b in enumerate(buttons):
        try:
            txt = b.inner_text().strip()
            if txt:
                print(f"Button {i}:", ascii(txt))
        except Exception:
            pass
            
    context.close()
