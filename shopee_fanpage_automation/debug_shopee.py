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
        args=["--start-maximized"]
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto(target_url, wait_until="domcontentloaded")
    time.sleep(5)
    
    print("URL:", page.url)
    print("Title:", ascii(page.title()))
    
    screenshot_path = r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\debug_page.png"
    page.screenshot(path=screenshot_path)
    print("Screenshot saved!")
    
    buttons = page.locator("button").all()
    print("Buttons count:", len(buttons))
    for i, b in enumerate(buttons):
        try:
            txt = b.inner_text().strip()
            print(f"Button {i}:", ascii(txt))
        except Exception as e:
            print(f"Button {i} err:", e)
            
    # Search elements with text 'Lấy link'
    elements = page.locator("text='Lấy link'").all()
    print("Elements with 'Lấy link':", len(elements))
    
    context.close()
