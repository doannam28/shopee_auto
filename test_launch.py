import time
from playwright.sync_api import sync_playwright

profile_dir = r"C:\Users\Admin\.gemini\antigravity\scratch\chrome_aff_profile"

with sync_playwright() as p:
    print("Launching persistent Chrome context...")
    context = p.chromium.launch_persistent_context(
        profile_dir,
        channel="chrome",
        headless=False,
        args=["--start-maximized"]
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://affiliate.shopee.vn")
    print("Current URL:", page.url)
    time.sleep(5)
    context.close()
    print("Closed successfully!")
