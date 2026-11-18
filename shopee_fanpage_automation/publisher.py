# -*- coding: utf-8 -*-
"""
Script hỗ trợ tự động:
1. Sinh link Shopee Affiliate từ URL gốc qua GraphQL Open API của Shopee.
2. Đăng bài viết (text + link + ảnh nếu có) lên Facebook Fanpage qua Graph API.
"""
import sys
import io
import time
import hashlib
import json
import urllib.request
import urllib.parse

# Đảm bảo console Windows in được tiếng Việt UTF-8
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import config
except ImportError:
    from . import config

def generate_shopee_affiliate_link(product_url: str) -> str:
    """Sinh shortlink tiếp thị liên kết Shopee thông qua Affiliate Open API"""
    if not config.SHOPEE_APP_ID or config.SHOPEE_APP_ID == "YOUR_SHOPEE_APP_ID":
        # Fallback khi chưa cấu hình API key
        return f"{product_url}?utm_source=an_affiliate"
    
    timestamp = int(time.time())
    query = """
    mutation {
        generateShortLink(input: { originUrl: "%s", subIds: ["fanpage_daily"] }) {
            shortLink
        }
    }
    """ % product_url
    
    payload = json.dumps({"query": query}).encode('utf-8')
    factor = f"{config.SHOPEE_APP_ID}{timestamp}{payload.decode('utf-8')}{config.SHOPEE_SECRET}"
    signature = hashlib.sha256(factor.encode('utf-8')).hexdigest()
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"SHA256 Credential={config.SHOPEE_APP_ID}, Timestamp={timestamp}, Signature={signature}"
    }
    
    req = urllib.request.Request("https://open-api.affiliate.shopee.vn/graphql", data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data.get("data", {}).get("generateShortLink", {}).get("shortLink", product_url)
    except Exception as e:
        print(f"Lỗi khi gọi Shopee Affiliate API: {e}")
        return product_url

def post_to_facebook_page(message: str, link: str = None) -> dict:
    """Đăng bài viết lên Fanpage bằng Page Access Token"""
    if not config.FB_PAGE_ACCESS_TOKEN or config.FB_PAGE_ACCESS_TOKEN == "YOUR_FACEBOOK_PAGE_ACCESS_TOKEN":
        print("[MÔ PHỎNG] Chưa điền Token Facebook thực tế. Nội dung bài viết mẫu:")
        print("------------------------------------------")
        print(message)
        if link:
            print(f"Link đính kèm: {link}")
        print("------------------------------------------")
        return {"status": "mock", "message": "Chưa có Token, đã mô phỏng thành công"}
    
    url = f"https://graph.facebook.com/v19.0/{config.FB_PAGE_ID}/feed"
    data = {
        "message": message,
        "access_token": config.FB_PAGE_ACCESS_TOKEN
    }
    if link:
        data["link"] = link
        
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(url, data=encoded_data, method='POST')
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Lỗi khi đăng bài lên Fanpage: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    sample_text = "🔥 Sản phẩm siêu hot hôm nay dành cho các bạn! 🔥\n👉 Xem ngay tại link bên dưới!"
    res = post_to_facebook_page(sample_text, "https://shopee.vn/sample-product")
    print("Kết quả:", res)
