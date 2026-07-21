import os
import glob

def fix_colors():
    template_dir = r"c:\Users\LENOVO\Desktop\krushi_mitra\krushi_mitra\subadmin\templates\subadmin"
    files = glob.glob(os.path.join(template_dir, "*.html"))
    
    replacements = [
        ("color:var(--gray-100)", "color:var(--gray-800)"),
        ("color:#fff", "color:var(--white)"),
        ("color: #fff", "color:var(--white)"),
        ("color: white", "color:var(--white)"),
        ("color:white", "color:var(--white)"),
        ("background:var(--card-bg)", "background:var(--white)"),
        ("background:var(--main-bg)", "background:var(--gray-50)"),
        ("var(--border)", "var(--gray-200)"),
        ("rgba(255,255,255,.05)", "var(--gray-50)"),
        ("rgba(255,255,255,.04)", "var(--gray-50)"),
        ("rgba(255,255,255,.08)", "var(--gray-100)"),
        ("rgba(255,255,255,0.05)", "var(--gray-50)"),
        ("rgba(255,255,255,0.1)", "var(--gray-100)"),
        ("rgba(255,255,255,0.2)", "var(--gray-200)"),
    ]
    
    # Exceptions where text should remain white because background is dark
    # For example, sidebars or specific dark sections.
    # But wait, we should only replace inline colors if they are actually wrong.
    # color:#fff on a dark gradient is CORRECT. E.g. <span style="background:linear-gradient(...);color:#fff;">
    # So blindly replacing #fff with var(--white) is fine because var(--white) is #fff.
    # BUT wait, the issue is that in some places `color:var(--gray-100)` makes text INVISIBLE.
    
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        new_content = content
        for old, new in replacements:
            new_content = new_content.replace(old, new)
            
        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(fpath)}")

if __name__ == "__main__":
    fix_colors()
