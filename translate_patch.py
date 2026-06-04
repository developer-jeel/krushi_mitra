import os
import re
import json

base_dirs = [
    r"c:\Users\LENOVO\Desktop\krushi_mitra\krushi_mitra\farmer\templates\farmer",
    r"c:\Users\LENOVO\Desktop\krushi_mitra\krushi_mitra\farmer\templates\buyer"
]

translations_to_add = {}

def camel_case(s):
    s = re.sub(r'[^a-zA-Z0-9 ]', '', s).strip()
    words = s.split()
    if not words:
        return "emptyKey"
    res = words[0].lower() + ''.join(w.capitalize() for w in words[1:])
    return res[:30]

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    pattern = re.compile(r'(<(div|span|button|a|th|td|label|p|h[1-6]|option|strong|b)[^>]*?>)([^<>\n]+)(</\2>)')
    
    def replacer(match):
        open_tag = match.group(1)
        tag_name = match.group(2)
        text = match.group(3).strip()
        close_tag = match.group(4)
        
        if 'data-translate' in open_tag or not text or '{' in text or '}' in text:
            return match.group(0)
            
        if text.isdigit() or text.startswith('?') or '?' in text or text.startswith('#') or '2026' in text:
            return match.group(0)
            
        key = camel_case(text)
        if not key or key == "emptyKey":
            return match.group(0)
            
        translations_to_add[key] = text
        
        new_open_tag = open_tag.replace('>', f' data-translate="{key}">', 1)
        return f"{new_open_tag}{match.group(3)}{close_tag}"

    new_html = pattern.sub(replacer, html)
    
    ph_pattern = re.compile(r'(<input[^>]*?placeholder=")([^"]+?)("[^>]*?>)')
    def ph_replacer(match):
        pre = match.group(1)
        text = match.group(2)
        post = match.group(3)
        if 'data-translate' in pre or 'data-translate' in post:
            return match.group(0)
            
        key = camel_case(text)
        if not key or key == "emptyKey":
            return match.group(0)
        translations_to_add[key] = text
        return f"{pre}{text}{post}".replace('<input ', f'<input data-translate="{key}" ')

    new_html = ph_pattern.sub(ph_replacer, new_html)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

for d in base_dirs:
    for filename in os.listdir(d):
        if filename.endswith(".html"):
            process_html_file(os.path.join(d, filename))

# Now update language.js
lang_js_path = r"c:\Users\LENOVO\Desktop\krushi_mitra\krushi_mitra\farmer\static\farmer\js\language.js"
with open(lang_js_path, 'r', encoding='utf-8') as f:
    lang_js = f.read()

# find the en: { ... } block
start_idx = lang_js.find('en: {')
end_idx = lang_js.find('},', start_idx)

en_block = lang_js[start_idx:end_idx]

# append translations_to_add
new_keys_str = ""
for k, v in translations_to_add.items():
    # prevent duplicate keys if they already exist
    if f"{k}:" not in en_block and f'"{k}":' not in en_block:
        safe_val = v.replace('"', '\\"')
        new_keys_str += f',\n    {k}: "{safe_val}"'

new_en_block = en_block + new_keys_str
new_lang_js = lang_js[:start_idx] + new_en_block + lang_js[end_idx:]

with open(lang_js_path, 'w', encoding='utf-8') as f:
    f.write(new_lang_js)

print("Updated language.js successfully.")
