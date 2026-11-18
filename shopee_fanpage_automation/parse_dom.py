import re

with open(r'C:\Users\Admin\.gemini\antigravity\scratch\shopee_fanpage_automation\dom.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print('Length:', len(text))
title = re.search(r'<title>(.*?)</title>', text)
print('Title:', ascii(title.group(1)) if title else 'None')

h1 = re.search(r'<h1[^>]*>(.*?)</h1>', text)
print('H1:', ascii(h1.group(1)) if h1 else 'None')

# Find product title spans or divs
spans = re.findall(r'<span[^>]*>(.*?)</span>', text)
for s in spans:
    if len(s) > 20 and ('giá' in s.lower() or 'bình' in s.lower() or 'máy' in s.lower() or 'áo' in s.lower() or 'quần' in s.lower() or 'túi' in s.lower()):
        print('SPAN:', ascii(s[:100]))

mp4s = re.findall(r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*', text)
print('MP4s:', set(mp4s))

cvfs = re.findall(r'https?://[^\s"\'<>]*cvf[^\s"\'<>]*', text)
print('CVFs:', set(cvfs))

# Search for any video tag
videos = re.findall(r'<video[^>]*>.*?</video>', text, re.DOTALL)
print('Video tags count:', len(videos))
for v in videos:
    print('VIDEO TAG:', ascii(v[:200]))
