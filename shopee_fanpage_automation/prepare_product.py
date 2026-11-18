import subprocess
import re
import requests
import os

url = "https://shopee.vn/product/20225722/24423345701"
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [edge_path, "--headless=new", "--disable-gpu", "--dump-dom", url]

print("Fetching product DOM...")
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
html = res.stdout

title_match = re.search(r'<title>(.*?)</title>', html)
title = title_match.group(1) if title_match else "Sản phẩm Shopee"
print("TITLE:", ascii(title))

mp4s = list(set(re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', html)))
print("Found MP4s:", mp4s)

if mp4s:
    video_url = mp4s[0]
    # Clean any trailing backslashes
    video_url = video_url.rstrip('\\')
    print("Downloading video:", video_url)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://shopee.vn/'
    }
    r = requests.get(video_url, headers=headers, stream=True)
    save_path = r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\product_video_next.mp4"
    if r.status_code == 200:
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk: f.write(chunk)
        print("Video downloaded successfully:", save_path, "Size:", os.path.getsize(save_path))
    else:
        print("Failed to download video. Status:", r.status_code)
else:
    print("No video found for this product.")
