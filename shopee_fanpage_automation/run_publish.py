# -*- coding: utf-8 -*-
import sys
sys.path.append(r'C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation')
from reel_publisher import upload_and_publish_reel

video_path = r'C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\product_video.mp4'

# Cấu trúc caption chuẩn: ĐƯA LINK AFFILIATE LÊN DÒNG ĐẦU TIÊN
caption = """👉 Link Shopee: https://s.shopee.vn/8AXQXfovcF

🚗 ĐỆM Ô TÔ GHẾ SAU GẤP GỌN BẰNG DA CAO CẤP - TIỆN LỢI CHO MỌI CHUYẾN ĐI! 🚗

✨ Biến băng ghế sau thành chiếc giường êm ái chỉ trong 30 giây!
✔️ Chất liệu da cao cấp, chống thấm nước, dễ dàng lau chùi vệ sinh.
✔️ Thiết kế gấp gọn thông minh, không chiếm diện tích khi không sử dụng.
✔️ Phù hợp cho cả gia đình, đặc biệt là người già và trẻ nhỏ khi đi đường dài.

📦 Freeship toàn quốc - Nhận hàng kiểm tra thoải mái!

#ShopeeAffiliate #DemOTo #NemXeHoi #PhuKienOTo #TapHoaMiaBo #ReelsDaily #MuaSamThongMinh"""

if __name__ == "__main__":
    res = upload_and_publish_reel(video_path, caption)
    print("FINAL RESULT:", res)
