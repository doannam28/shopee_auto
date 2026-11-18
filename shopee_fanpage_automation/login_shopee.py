# -*- coding: utf-8 -*-
import time
from playwright.sync_api import sync_playwright

PROFILE_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\chrome_aff_profile"

print("=" * 60)
print("[*] DANG MO CHROME DE DANG NHAP SHOPEE AFFILIATE...")
print("[*] Vui long dang nhap tai khoan Shopee cua ban tren cua so vua mo ra.")
print("[*] Sau khi dang nhap xong va thay trang chu Shopee Affiliate,")
print("[*] Phien dang nhap se duoc luu vinh vien cho Bot tu dong hoa!")
print("=" * 60)

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        PROFILE_DIR,
        channel="chrome",
        headless=False,
        args=["--start-maximized"]
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://affiliate.shopee.vn")
    
    # Cho nguoi dung dang nhap toi da 3 phut (180s) hoac khi vao duoc dashboard
    for i in range(180):
        time.sleep(1)
        if "dashboard" in page.url.lower() or "offer" in page.url.lower() or "home" in page.url.lower():
            if not ("login" in page.url.lower() or "auth" in page.url.lower()):
                print(f"[🎉] DA PHAT HIEN DANG NHAP THANH CONG! (URL: {page.url})")
                time.sleep(3)
                break
                
    context.close()
    print("[*] Da luu phien dang nhap Shopee Affiliate thanh cong!")
