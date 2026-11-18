import re

with open(r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\dom_product2.html", "w", encoding="utf-8") as f:
    import subprocess
    cmd = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "--headless=new", "--disable-gpu", "--dump-dom", "https://shopee.vn/product/20225722/24423345701"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    f.write(res.stdout)
    html = res.stdout

# Find spans or h1
for s in re.findall(r'<span[^>]*>(.*?)</span>', html):
    s_clean = re.sub(r'<[^>]+>', '', s).strip()
    if len(s_clean) > 20 and not 'shopee' in s_clean.lower() and not 'voucher' in s_clean.lower() and not 'javascript' in s_clean.lower():
        print("SPAN:", ascii(s_clean[:120]))
