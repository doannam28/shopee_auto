import re

with open(r"C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\dom_product2.html", "r", encoding="utf-8") as f:
    text = f.read()

# Look for json LD or schema.org
json_ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.DOTALL)
print("JSON-LD found:", len(json_ld))
for j in json_ld:
    print('JSON-LD:', ascii(j[:200]))

og_title = re.search(r'<meta[^>]+property=[\'"]og:title[\'"][^>]+content=[\'"](.*?)[\'"]', text)
if og_title:
    print('OG:TITLE:', ascii(og_title.group(1)))

meta_desc = re.search(r'<meta[^>]+name=[\'"]description[\'"][^>]+content=[\'"](.*?)[\'"]', text)
if meta_desc:
    print('META:DESC:', ascii(meta_desc.group(1)[:200]))

# Search for any product title pattern
match_p = re.findall(r'"name":"([^"]+)"', text)
print("Names found:", [ascii(n) for n in match_p if len(n) > 10][:5])
