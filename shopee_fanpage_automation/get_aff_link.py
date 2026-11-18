# -*- coding: utf-8 -*-
"""
Lấy link Affiliate Shopee từ Chrome đang mở (debug mode).
Cách dùng:
  1. Chạy Mo_Chrome_Debug_Shopee.bat trên Desktop
  2. Chạy script này: python get_aff_link.py <URL_SAN_PHAM>

Ví dụ:
  python get_aff_link.py https://shopee.vn/product/1803026561/51409283226
"""
import sys, io, time, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[!] Chua cai playwright. Chay: pip install playwright && playwright install chromium")
    sys.exit(1)

SHOPEE_AFF_HOME = "https://affiliate.shopee.vn/offer/product_selection"
CDP_URL = "http://localhost:9222"

def get_product_aff_link(product_url: str) -> str:
    """
    Kết nối Chrome đang mở, vào Shopee Affiliate,
    tạo link rút gọn cho sản phẩm và trả về.
    """
    # Tách shop_id và item_id từ URL
    m = re.search(r'product/(\d+)/(\d+)', product_url)
    if not m:
        raise ValueError(f"URL không hợp lệ: {product_url}")
    shop_id, item_id = m.group(1), m.group(2)
    
    print(f"[*] Shop ID: {shop_id} | Item ID: {item_id}")

    with sync_playwright() as p:
        print(f"[*] Ket noi Chrome tai {CDP_URL}...")
        try:
            browser = p.chromium.connect_over_cdp(CDP_URL)
        except Exception as e:
            print(f"[!] Khong the ket noi Chrome!")
            print(f"    -> Hay chay 'Mo_Chrome_Debug_Shopee.bat' truoc!")
            print(f"    Chi tiet loi: {e}")
            return None

        # Dùng context đầu tiên (phiên đăng nhập hiện tại)
        ctx = browser.contexts[0]
        page = ctx.new_page()

        # Vào trang tạo link affiliate của Shopee
        aff_url = f"https://affiliate.shopee.vn/offer/generate_affiliate_link"
        print(f"[*] Vao trang Shopee Affiliate...")
        page.goto("https://affiliate.shopee.vn/offer/product_selection", wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        # Kiểm tra đã đăng nhập chưa
        if "login" in page.url.lower():
            print("[!] Chua dang nhap Shopee Affiliate!")
            print("    -> Vui long dang nhap trong cua so Chrome vua mo, roi chay lai script.")
            page.close()
            return None

        # Dùng API Affiliate nội bộ để tạo link
        print(f"[*] Dang tao link affiliate cho san pham...")
        
        # Gọi API tạo link qua fetch trong browser context
        js_code = f"""
        async () => {{
            const resp = await fetch('https://affiliate.shopee.vn/api/v2/product/get_product_link', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'x-csrftoken': document.cookie.match(/csrftoken=([^;]+)/)?.[1] || ''
                }},
                body: JSON.stringify({{
                    item_id: {item_id},
                    shop_id: {shop_id},
                    link_type: 2
                }})
            }});
            const data = await resp.json();
            return JSON.stringify(data);
        }}
        """
        result = page.evaluate(js_code)
        print(f"[*] Ket qua API: {result}")

        import json
        try:
            data = json.loads(result)
            # Tìm link rút gọn trong response
            if data.get("data") and data["data"].get("short_link"):
                link = data["data"]["short_link"]
                print(f"[+] LINK AFF: {link}")
                page.close()
                return link
        except:
            pass

        # Fallback: thử cách khác - dùng trang generate link
        print("[*] Thu cach khac - generate link truc tiep...")
        gen_url = f"https://affiliate.shopee.vn/offer/generate_affiliate_link?url={product_url}"
        page.goto(gen_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)
        
        # Tìm input chứa link rút gọn
        try:
            inp = page.query_selector('input[readonly]')
            if inp:
                link = inp.input_value()
                if link.startswith("http"):
                    print(f"[+] LINK AFF: {link}")
                    page.close()
                    return link
        except:
            pass

        print("[!] Khong the lay duoc link. Chup man hinh de debug...")
        page.screenshot(path=r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\debug_aff.png")
        page.close()
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cach dung: python get_aff_link.py <URL_SAN_PHAM_SHOPEE>")
        print("Vi du:     python get_aff_link.py https://shopee.vn/product/1803026561/51409283226")
        sys.exit(1)
    
    product_url = sys.argv[1]
    print("=" * 60)
    print(f"[*] San pham: {product_url}")
    link = get_product_aff_link(product_url)
    if link:
        print("=" * 60)
        print(f"✅ LINK AFFILIATE: {link}")
        print("=" * 60)
        # Lưu vào clipboard nếu có
        try:
            import subprocess
            subprocess.run(['clip'], input=link.encode('utf-8'), check=True)
            print("(Da copy vao Clipboard!)")
        except:
            pass
    else:
        print("[!] Khong lay duoc link affiliate.")
