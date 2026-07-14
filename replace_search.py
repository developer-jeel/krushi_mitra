import os
import glob
import re

template_dir = r"c:\Users\LENOVO\Desktop\krushi_mitra\krushi_mitra\buyer\templates\buyer"
html_files = glob.glob(os.path.join(template_dir, "*.html"))

# We want to find: <div class="search-box" ... > ... <input type="text" ... > ... </div>
# And replace it with a form that submits to buyer_browse_crops.
# Since it might be multiline, we'll use a regex.

pattern = re.compile(r'<div class="search-box"[^>]*>.*?<input type="text"[^>]*placeholder="([^"]+)"[^>]*>.*?</div>', re.DOTALL)

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    def replacer(match):
        placeholder = match.group(1)
        # keep the original placeholder but wrap in a form
        return f'''<form action="{{% url 'buyer_browse_crops' %}}" method="GET" style="display:inline;">
            <div class="search-box" data-search-target>
              <span class="search-icon">🔍</span>
              <input type="text" name="q" placeholder="{placeholder}" aria-label="Search" value="{{{{ request.GET.q|default:'' }}}}">
            </div>
          </form>'''
          
    new_content, count = pattern.subn(replacer, content)
    
    if count > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated search box in {os.path.basename(file_path)}")

print("Done replacing search boxes.")
