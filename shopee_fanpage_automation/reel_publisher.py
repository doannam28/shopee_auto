# -*- coding: utf-8 -*-
"""
Module tự động đăng video Reels lên Facebook Fanpage
Sử dụng Facebook Reels Publishing API
"""
import sys
import os
import requests
import config

def upload_and_publish_reel(video_file_path: str, caption: str) -> dict:
    """
    Quy trình 3 bước đăng Facebook Reel:
    Bước 1: Khởi tạo phiên upload (upload_phase = start)
    Bước 2: Upload file nhị phân (binary) lên upload_url
    Bước 3: Hoàn tất và xuất bản Reel (upload_phase = finish)
    """
    if not os.path.exists(video_file_path):
        return {"error": f"Không tìm thấy file video: {video_file_path}"}
    
    file_size = os.path.getsize(video_file_path)
    page_id = config.FB_PAGE_ID
    access_token = config.FB_PAGE_ACCESS_TOKEN
    
    print(f"[*] Bat dau tao Reel tren Page {page_id}...")
    print(f"[*] Kich thuoc video: {file_size / 1024 / 1024:.2f} MB")
    
    # Bước 1: Khởi tạo
    start_url = f"https://graph.facebook.com/v19.0/{page_id}/video_reels"
    start_payload = {
        "upload_phase": "start",
        "access_token": access_token
    }
    
    start_res = requests.post(start_url, data=start_payload)
    if start_res.status_code != 200:
        return {"error": f"Loi khoi tao Reel: {start_res.text}"}
    
    start_data = start_res.json()
    video_id = start_data.get("video_id")
    upload_url = start_data.get("upload_url")
    
    print(f"[+] Khoi tao thanh cong! Video ID: {video_id}")
    
    # Bước 2: Tải video lên binary
    headers = {
        "Authorization": f"OAuth {access_token}",
        "offset": "0",
        "file_size": str(file_size)
    }
    
    with open(video_file_path, "rb") as f:
        video_bytes = f.read()
        
    upload_res = requests.post(upload_url, headers=headers, data=video_bytes)
    if upload_res.status_code not in (200, 201):
        return {"error": f"Loi upload video binary: {upload_res.text}"}
        
    print(f"[+] Da tai du lieu video len Facebook thanh cong!")
    
    # Bước 3: Xuất bản Reel
    finish_url = f"https://graph.facebook.com/v19.0/{page_id}/video_reels"
    finish_payload = {
        "upload_phase": "finish",
        "access_token": access_token,
        "video_id": video_id,
        "video_state": "PUBLISHED",
        "description": caption
    }
    
    finish_res = requests.post(finish_url, data=finish_payload)
    if finish_res.status_code != 200:
        return {"error": f"Loi xuat ban Reel: {finish_res.text}"}
        
    res_json = finish_res.json()
    if isinstance(res_json, dict) and "post_id" not in res_json:
        res_json["post_id"] = video_id
    print(f"[+] Reel da duoc xuat ban thanh cong! Ket qua: {res_json}")
    return res_json

if __name__ == "__main__":
    sample_video = r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\product_video.mp4"
    caption = "Test reel"
    result = upload_and_publish_reel(sample_video, caption)
    print("KET QUA:", result)
