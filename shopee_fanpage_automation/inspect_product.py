import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
}
r = requests.get('https://s.shopee.vn/8AXQXfovcF', headers=headers, allow_redirects=True)
html = r.text

with open('page.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Status:', r.status_code)
print('Final URL:', r.url)

for line in html.split('\n'):
    if 'og:title' in line or 'og:description' in line or 'og:image' in line or 'og:video' in line:
        print(ascii(line.strip()))

# Search for video URLs
mp4_links = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', html)
print('MP4 links:', mp4_links)

cvf_links = re.findall(r'https?://[^\s"\'<>]*cvf[^\s"\'<>]*', html)
print('CVF links:', cvf_links)
