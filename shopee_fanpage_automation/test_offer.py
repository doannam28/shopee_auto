# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

PROFILE_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\chrome_aff_profile"

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
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    
    # 1. Truy cap trang chu affiliate truoc
    print("Navigating to home...")
    page.goto("https://affiliate.shopee.vn", wait_until="domcontentloaded")
    time.sleep(3)
    print("Home URL:", page.url)
    
    # 2. Truy cap trang product offer
    print("Navigating to product offer...")
    page.goto("https://affiliate.shopee.vn/offer/product_offer/24964977977", wait_until="domcontentloaded")
    time.sleep(5)
    print("Offer URL:", page.url)
    
    page.screenshot(path=r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\debug_offer.png")
    
    # Check buttons
    buttons = page.locator("button, a").all()
    print("Total buttons/links:", len(buttons))
    found = False
    for b in buttons:
        try:
            txt = b.inner_text().strip()
            if "lấy link" in txt.lower():
                print("FOUND BUTTON:", ascii(txt))
                found = True
                b.click()
                time.sleep(2)
                page.screenshot(path=r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\debug_popup.png")
                # Look for input
                for inp in page.locator("input, textarea").all():
                    val = inp.input_value()
                    if "s.shopee.vn" in val:
                        print("AFFILIATE SHORTLINK:", val)
                break
        except Exception:
            pass
            
    if not found:
        print("Could not find 'Lấy link' button.")
        
    context.close()
