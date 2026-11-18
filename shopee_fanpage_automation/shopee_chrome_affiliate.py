# -*- coding: utf-8 -*-
"""
Module tự động trích xuất Link Shopee Affiliate qua Chrome Browser Automation (Playwright Persistent Context)
Sử dụng profile Chrome tự động hóa chuyên biệt: C:\\Users\\Admin\\.gemini\\antigravity\\scratch\\chrome_aff_profile
"""
import sys
import os
import re
import time
from playwright.sync_api import sync_playwright

PROFILE_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\chrome_aff_profile"

def get_affiliate_link_from_chrome(item_id_or_url: str, headless: bool = False) -> str:
    """
    Mở Chrome tự động hóa, truy cập affiliate.shopee.vn/offer/product_offer/{item_id},
    bấm 'Lấy link', trích xuất link rút gọn https://s.shopee.vn/... và đóng trình duyệt.
    """
    # 1. Trích xuất item_id
    if isinstance(item_id_or_url, str) and ("shopee.vn" in item_id_or_url or "/" in item_id_or_url):
        match = re.search(r"i\.[0-9]+\.([0-9]+)", item_id_or_url)
        if not match:
            match = re.search(r"/([0-9]{8,})", item_id_or_url)
        if match:
            item_id = match.group(1)
        else:
            item_id = item_id_or_url.split("/")[-1].split("?")[0]
    else:
        item_id = str(item_id_or_url)
        
    target_url = f"https://affiliate.shopee.vn/offer/product_offer/{item_id}"
    print(f"[*] Muc tieu: {target_url}")
    
    with sync_playwright() as p:
        print("[*] Dang khoi dong Chrome tu dong hoa...")
        context = p.chromium.launch_persistent_context(
            PROFILE_DIR,
            channel="chrome",
            headless=headless,
            args=["--start-maximized"]
        )
        page = context.pages[0] if context.pages else context.new_page()
        
        try:
            print(f"[*] Dang tai trang hoa hong san pham: {target_url}...")
            page.goto(target_url, wait_until="domcontentloaded", timeout=45000)
            
            # Kiểm tra xem có đang bị chuyển hướng tới trang đăng nhập không
            time.sleep(3)
            current_url = page.url
            if "login" in current_url.lower() or "auth" in current_url.lower():
                print(f"[!] Can dang nhap tai khoan Shopee Affiliate tren profile nay truoc!")
                print(f"[!] Vui long dang nhap tren cua so Chrome dang hien thi...")
                # Cho nguoi dung dang nhap trong 60 giay
                for _ in range(60):
                    time.sleep(1)
                    if "offer" in page.url:
                        break
            
            # 2. Tim nut 'Lay link'
            print("[*] Dang tim nut 'Lay link' tren giao dien Shopee Affiliate...")
            lay_link_btn = None
            
            # Thu cac selector nut 'Lay link'
            selectors = [
                "button:has-text('Lấy link')",
                "button:has-text('Lay link')",
                ".shopee-button:has-text('Lấy link')",
                "text='Lấy link'"
            ]
            for sel in selectors:
                try:
                    btn = page.locator(sel).first
                    if btn.is_visible():
                        lay_link_btn = btn
                        break
                except Exception:
                    pass
                    
            if not lay_link_btn:
                print("[!] Chua tim thay nut 'Lay link'. Cho them 5 giay...")
                time.sleep(5)
                lay_link_btn = page.locator("button:has-text('Lấy link')").first
                
            lay_link_btn.click()
            print("[+] Da click vao nut 'Lay link'!")
            
            # 3. Cho popup xuat hien va trich xuat link rut gon
            time.sleep(2)
            short_link = None
            
            # Kiem tra trong input/textarea cua popup
            inputs = page.locator("input, textarea").all()
            for inp in inputs:
                try:
                    val = inp.input_value()
                    if val and "s.shopee.vn" in val:
                        short_link = val.strip()
                        break
                except Exception:
                    pass
                    
            if not short_link:
                # Tim chuoi text truc tiep
                elem = page.locator("text=/https:\\/\\/s\\.shopee\\.vn\\/[a-zA-Z0-9]+/").first
                if elem.is_visible():
                    short_link = elem.inner_text().strip()
                    
            if short_link:
                print(f"[+] Trich xuat link Affiliate thanh cong: {short_link}")
                return short_link
            else:
                print("[!] Khong doc duoc link tu popup.")
                return None
                
        except Exception as e:
            print(f"[!] Loi: {e}")
            return None
        finally:
            context.close()
            print("[*] Da dong trinh duyet Chrome tu dong hoa.")

if __name__ == "__main__":
    link = get_affiliate_link_from_chrome("24964977977", headless=False)
    print("KET QUA LINK:", link)
