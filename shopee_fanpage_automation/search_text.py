import re

with open(r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\dom_product2.html", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

matches = re.findall(r'"([^"]{10,100})"', text)
vietnamese_matches = []
for m in matches:
    if any(c in m.lower() for c in 'àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ'):
        vietnamese_matches.append(m)

print('Vietnamese text matches:', len(vietnamese_matches))
for v in vietnamese_matches[:15]:
    print('->', ascii(v))
