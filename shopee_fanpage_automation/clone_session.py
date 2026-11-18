import shutil
import os

src_base = r"C:\Users\Admin\AppData\Local\Google\Chrome\User Data"
dst_base = r"C:\Users\Admin\.gemini\antigravity\scratch\chrome_aff_profile"

os.makedirs(dst_base, exist_ok=True)

# Copy Local State
shutil.copy2(os.path.join(src_base, "Local State"), os.path.join(dst_base, "Local State"))
print("Copied Local State.")

src_default = os.path.join(src_base, "Default")
dst_default = os.path.join(dst_base, "Default")
os.makedirs(dst_default, exist_ok=True)

# Copy Network\Cookies
src_cookies = os.path.join(src_default, "Network", "Cookies")
dst_network = os.path.join(dst_default, "Network")
os.makedirs(dst_network, exist_ok=True)
if os.path.exists(src_cookies):
    shutil.copy2(src_cookies, os.path.join(dst_network, "Cookies"))
    print("Copied Cookies.")

# Copy Local Storage if exists
src_ls = os.path.join(src_default, "Local Storage")
dst_ls = os.path.join(dst_default, "Local Storage")
if os.path.exists(src_ls):
    if os.path.exists(dst_ls): shutil.rmtree(dst_ls)
    shutil.copytree(src_ls, dst_ls)
    print("Copied Local Storage.")

print("Session clone completed successfully!")
