# -*- coding: utf-8 -*-
"""
Module trích xuất và tải video từ Shopee
Hỗ trợ cả link Shopee video và link sản phẩm Shopee có video
"""
import re
import os
import requests

def extract_ids_from_shopee_url(url: str):
    """Trích xuất shop_id và item_id từ URL Shopee"""
    match = re.search(r"i\.([0-9]+)\.([0-9]+)", url)
    if match:
        return match.group(1), match.group(2)
    
    # Xử lý link rút gọn như shp.ee hoặc s.shopee.co
    if "shp.ee" in url or "s.shopee.co" in url or "shopee.vn/universal-link" in url:
        try:
            r = requests.get(url, allow_redirects=True, timeout=10)
            match = re.search(r"i\.([0-9]+)\.([0-9]+)", r.url)
            if match:
                return match.group(1), match.group(2)
        except Exception:
            pass
    return None, None

def download_video_from_url(video_url: str, output_path: str) -> bool:
    """Tải trực tiếp video từ URL bất kỳ về máy"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(video_url, headers=headers, stream=True, timeout=30)
        if r.status_code == 200:
            with open(output_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            return True
    except Exception as e:
        print(f"Lỗi khi tải video: {e}")
    return False
