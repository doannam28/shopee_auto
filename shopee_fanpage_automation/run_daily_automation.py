# -*- coding: utf-8 -*-
"""
Kịch bản chạy tự động hàng ngày lúc 8h sáng:
1. Đọc sản phẩm tiếp theo từ queue.json
2. Kiểm tra xem URL đã đăng chưa (posted_urls.json)
3. Đăng Reel lên Fanpage Tạp hóa Mía Bơ với link Affiliate ở dòng đầu tiên
4. Lưu URL vào posted_urls.json để tránh đăng trùng
"""
import sys, os, json, io
from datetime import datetime

# Fix encoding tiếng Việt trên Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation"
sys.path.insert(0, SCRIPT_DIR)

from reel_publisher import upload_and_publish_reel

QUEUE_FILE = os.path.join(SCRIPT_DIR, "queue.json")
POSTED_URLS_FILE = os.path.join(SCRIPT_DIR, "posted_urls.json")

# ─── Quản lý danh sách URL đã đăng ──────────────────────────────────────────

def load_posted_urls():
    """Đọc danh sách URL đã đăng từ posted_urls.json"""
    if not os.path.exists(POSTED_URLS_FILE):
        return []
    with open(POSTED_URLS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def is_already_posted(product_url):
    """Kiểm tra URL sản phẩm đã được đăng chưa"""
    posted = load_posted_urls()
    posted_urls = [p["product_url"] for p in posted]
    return product_url in posted_urls

def save_to_posted_urls(item, post_id):
    """Lưu URL vào posted_urls.json sau khi đăng thành công"""
    posted = load_posted_urls()
    posted.append({
        "product_url": item["product_url"],
        "product_name": item["product_name"],
        "aff_link": item["aff_link"],
        "posted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "post_id": str(post_id)
    })
    with open(POSTED_URLS_FILE, "w", encoding="utf-8") as f:
        json.dump(posted, f, ensure_ascii=False, indent=2)
    print(f"[+] Da luu URL vao posted_urls.json (tong cong: {len(posted)} san pham)")

# ─── Quản lý queue ───────────────────────────────────────────────────────────

def get_next_product():
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)
    for item in queue:
        if not item.get("posted", False):
            return queue, item
    return queue, None

def mark_posted(queue, item):
    for q in queue:
        if q["product_url"] == item["product_url"]:
            q["posted"] = True
            q["posted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

def build_caption(item):
    name = item["product_name"]
    aff_link = item["aff_link"]
    name_lower = name.lower()
    if "giày" in name_lower:
        icon = "👟"
    elif "đèn" in name_lower:
        icon = "🔦"
    elif "đệm" in name_lower:
        icon = "🚗"
    else:
        icon = "🔥"
    return f"""👉 Link Shopee: {aff_link}

{icon} {name.upper()}

✨ Đây là sản phẩm chất lượng cao đang được nhiều người săn đón!
✔️ Chính hãng 100%, bảo hành đầy đủ.
✔️ Giao hàng nhanh toàn quốc, nhận hàng kiểm tra.
✔️ Giá tốt nhất thị trường - Mua ngay kẻo hết!

📦 Freeship toàn quốc - Shopee đảm bảo!

#ShopeeAffiliate #TapHoaMiaBo #DealHot #MuaSamThongMinh #ReelsDaily"""

def run():
    print("=" * 60)
    print("[*] BAT DAU AUTOMATION 8H SANG...")
    queue, item = get_next_product()
    
    if not item:
        print("[!] Khong con san pham nao trong hang doi. Vui long them san pham moi vao queue.json!")
        return
    
    print(f"[*] San pham: {item['product_name']}")
    print(f"[*] Link Aff: {item['aff_link']}")
    
    # ── KIỂM TRA TRÙNG LẶP ──────────────────────────────────────
    if is_already_posted(item["product_url"]):
        print(f"[!] CANH BAO: San pham nay DA DANG ROI!")
        print(f"    URL: {item['product_url']}")
        print("[!] Bo qua de tranh dang trung. Vui long them san pham moi vao queue.json!")
        return
    # ─────────────────────────────────────────────────────────────
    
    video_path = os.path.join(SCRIPT_DIR, item["video_file"])
    if not os.path.exists(video_path):
        print(f"[!] Khong tim thay file video: {video_path}")
        return
    
    caption = build_caption(item)
    print("[*] Dang dang Reel len Fanpage...")
    res = upload_and_publish_reel(video_path, caption)
    
    if res.get("success") or res.get("post_id"):
        mark_posted(queue, item)
        save_to_posted_urls(item, res.get("post_id", "unknown"))  # Lưu vào danh sách chống trùng
        print("[+] DANG BAI THANH CONG! Post ID:", res.get("post_id", res))
    else:
        print("[!] DANG BAI THAT BAI:", res)

if __name__ == "__main__":
    run()
