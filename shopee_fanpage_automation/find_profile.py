import sqlite3, os, shutil
base = r'C:\Users\Admin\AppData\Local\Google\Chrome\User Data'
for p in ['Profile 10', 'Profile 5', 'Default']:
    hist_src = os.path.join(base, p, 'History')
    if not os.path.exists(hist_src): continue
    tmp_hist = 'temp_hist.db'
    try:
        shutil.copy2(hist_src, tmp_hist)
        conn = sqlite3.connect(tmp_hist)
        cur = conn.cursor()
        cur.execute("SELECT url FROM urls WHERE url LIKE '%affiliate.shopee%' ORDER BY last_visit_time DESC LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if os.path.exists(tmp_hist): os.remove(tmp_hist)
        print(p, '->', row[0] if row else 'None')
    except Exception as e:
        print(p, 'Error:', e)
