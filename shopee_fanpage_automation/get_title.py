import requests
import re

r = requests.get('https://s.shopee.vn/9pfealw3ea', headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
url = r.url
print("Final URL:", url)

# Extract product slug from URL
# e.g. https://shopee.vn/Ten-San-Pham-i.xxx.yyy
match = re.search(r'shopee\.vn/([^/?]+)-i\.', url)
if match:
    slug = match.group(1).replace('-', ' ')
    print("SLUG NAME:", slug)
else:
    # try another pattern
    match2 = re.search(r'shopee\.vn/([^/?]+)/', url)
    if match2:
        print("SLUG 2:", match2.group(1))
