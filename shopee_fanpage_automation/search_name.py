import re

with open(r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\dom_product2.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Extract all JSON blocks in script tag at the top
scripts = re.findall(r'<script[^>]*>(.*?)</script>', text, re.DOTALL)
import json
for s in scripts:
    if 'item' in s.lower() and len(s) > 1000:
        # Look for product name pattern
        name_pattern = re.findall(r'"name"\s*:\s*"([^"]{10,200})"', s)
        for n in name_pattern:
            if any(c in n for c in 'àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ') or len(n) > 30:
                print("NAME:", ascii(n))
