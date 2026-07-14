import os
import glob

template_dir = r"c:\Users\LENOVO\Desktop\krushi_mitra\krushi_mitra\buyer\templates\buyer"
html_files = glob.glob(os.path.join(template_dir, "*.html"))

replacements = {
    '<div class="profile-avatar">RM</div>': '<div class="profile-avatar">{{ buyr.user.name|make_list|first|upper }}</div>',
    '<div class="profile-name">Rajesh Mehta</div>': '<div class="profile-name">{{ buyr.user.name }}</div>',
    '<div class="profile-role">Wholesale Trader</div>': '<div class="profile-role">{{ buyr.business_type|default:"Buyer" }}</div>',
    '🎉 Welcome back, Rajesh!': '🎉 Welcome back, {{ buyr.user.name }}!',
    'Welcome back, Rajesh!': 'Welcome back, {{ buyr.user.name }}!',
}

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    modified = False
    for old_str, new_str in replacements.items():
        if old_str in content:
            content = content.replace(old_str, new_str)
            modified = True
            
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {os.path.basename(file_path)}")

print("Done replacing placeholders.")
