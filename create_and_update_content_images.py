import os
import django
import random
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'krushi_mitra.settings')
django.setup()

from farmer.models import bloag, news, gov_info

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(BASE_DIR, 'media', 'bloag', 'images')
NEWS_DIR = os.path.join(BASE_DIR, 'media', 'news', 'images')
GOV_DIR = os.path.join(BASE_DIR, 'media', 'gov_info', 'images')

os.makedirs(BLOG_DIR, exist_ok=True)
os.makedirs(NEWS_DIR, exist_ok=True)
os.makedirs(GOV_DIR, exist_ok=True)

# Theme palettes (bg_start, bg_end, accent_color, category_label)
THEMES = {
    'organic': {'bg1': (20, 80, 45), 'bg2': (10, 45, 25), 'accent': (74, 222, 128), 'tag': 'Organic & Soil'},
    'irrigation': {'bg1': (15, 70, 110), 'bg2': (10, 35, 60), 'accent': (56, 189, 248), 'tag': 'Water & Tech'},
    'market': {'bg1': (120, 70, 15), 'bg2': (65, 35, 10), 'accent': (251, 191, 36), 'tag': 'Market & Price'},
    'crop': {'bg1': (40, 90, 30), 'bg2': (20, 50, 15), 'accent': (134, 239, 172), 'tag': 'Crop Advisory'},
    'gov': {'bg1': (30, 58, 138), 'bg2': (15, 23, 42), 'accent': (96, 165, 250), 'tag': 'Government Scheme'},
    'news': {'bg1': (127, 29, 29), 'bg2': (69, 10, 10), 'accent': (248, 113, 113), 'tag': 'Agri News'},
    'weather': {'bg1': (14, 116, 144), 'bg2': (21, 67, 96), 'accent': (125, 211, 252), 'tag': 'Weather Alert'},
    'tech': {'bg1': (88, 28, 135), 'bg2': (46, 16, 101), 'accent': (192, 132, 252), 'tag': 'Agri Technology'},
    'dairy': {'bg1': (55, 65, 81), 'bg2': (31, 41, 55), 'accent': (229, 231, 235), 'tag': 'Dairy & Livestock'},
}

def get_font(size):
    for font_name in ["arial.ttf", "arialbd.ttf", "DejaVuSans.ttf"]:
        try:
            return ImageFont.truetype(font_name, size)
        except IOError:
            continue
    return ImageFont.load_default()

def create_banner_image(title, subtitle, category_key, output_filepath, width=800, height=480):
    theme = THEMES.get(category_key, THEMES['organic'])
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    bg1, bg2 = theme['bg1'], theme['bg2']
    accent = theme['accent']

    # Gradient background
    for y in range(height):
        ratio = y / height
        r = int(bg1[0] * (1 - ratio) + bg2[0] * ratio)
        g = int(bg1[1] * (1 - ratio) + bg2[1] * ratio)
        b = int(bg1[2] * (1 - ratio) + bg2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Abstract geometry background accents
    draw.ellipse([width - 240, -80, width + 120, 280], fill=(*accent, 25))
    draw.ellipse([-100, height - 200, 200, height + 100], fill=(*accent, 25))
    draw.ellipse([width // 2 - 100, height // 2 - 100, width // 2 + 100, height // 2 + 100], outline=(255, 255, 255), width=1)

    # Decorative Card Frame
    margin = 24
    draw.rectangle([margin, margin, width - margin, height - margin], outline=(255, 255, 255), width=2)

    # Category Pill
    pill_text = subtitle.upper() if subtitle else theme['tag'].upper()
    font_tag = get_font(16)
    bbox_tag = draw.textbbox((0, 0), pill_text, font=font_tag)
    tw, th = bbox_tag[2] - bbox_tag[0], bbox_tag[3] - bbox_tag[1]
    px, py = margin + 20, margin + 20
    draw.rectangle([px, py, px + tw + 24, py + th + 14], fill=accent)
    draw.text((px + 12, py + 7), pill_text, fill=(15, 23, 42), font=font_tag)

    # Title rendering (wrap if too long)
    font_title = get_font(28)
    words = title.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        line_str = " ".join(current_line)
        bbox = draw.textbbox((0, 0), line_str, font=font_title)
        if bbox[2] - bbox[0] > width - 100:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))

    # Draw title text centered vertically in remaining space
    text_y = height // 2 - (len(lines) * 36) // 2 + 10
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        tw = bbox[2] - bbox[0]
        tx = (width - tw) // 2
        # Text drop shadow
        draw.text((tx + 2, text_y + 2), line, fill=(0, 0, 0), font=font_title)
        draw.text((tx, text_y), line, fill=(255, 255, 255), font=font_title)
        text_y += 42

    # Brand Footer
    font_brand = get_font(15)
    brand = "KRUSHI MITRA • AGRICULTURE PORTAL"
    bbox_b = draw.textbbox((0, 0), brand, font=font_brand)
    bx = (width - (bbox_b[2] - bbox_b[0])) // 2
    draw.text((bx, height - margin - 26), brand, fill=(200, 225, 210), font=font_brand)

    img.save(output_filepath, 'JPEG', quality=92)

# Helper function to categorize titles
def categorize_title(title):
    t = title.lower()
    if 'drip' in t or 'water' in t or 'rain' in t or 'pump' in t or 'irrigation' in t:
        return 'irrigation'
    if 'organic' in t or 'fertilizer' in t or 'pest' in t or 'soil' in t:
        return 'organic'
    if 'rate' in t or 'price' in t or 'export' in t or 'mandi' in t or 'market' in t:
        return 'market'
    if 'scheme' in t or 'kisan' in t or 'subsidy' in t or 'gov' in t or 'yojana' in t:
        return 'gov'
    if 'weather' in t or 'monsoon' in t or 'rain' in t:
        return 'weather'
    if 'tech' in t or 'ai' in t or 'tool' in t or 'mechanization' in t:
        return 'tech'
    if 'dairy' in t or 'milk' in t:
        return 'dairy'
    return 'crop'

# 1. GENERATE BLOG IMAGES
print("--- Updating Blog Images ---")
blogs = bloag.objects.all()
for b in blogs:
    safe_name = "".join([c if c.isalnum() else "_" for c in b.title])[:30].strip("_")
    filename = f"blog_{b.id}_{safe_name}.jpg"
    filepath = os.path.join(BLOG_DIR, filename)
    cat = categorize_title(b.title)
    create_banner_image(b.title, "FARMING BLOG", cat, filepath)
    b.image = f"bloag/images/{filename}"
    b.save()
print(f"Successfully generated and assigned images for {blogs.count()} blogs.")

# 2. GENERATE GOV SCHEME IMAGES
print("\n--- Updating Gov Scheme Images ---")
schemes = gov_info.objects.all()
for g in schemes:
    safe_name = "".join([c if c.isalnum() else "_" for c in g.title])[:30].strip("_")
    filename = f"scheme_{g.id}_{safe_name}.jpg"
    filepath = os.path.join(GOV_DIR, filename)
    create_banner_image(g.title, "GOVT SCHEME", 'gov', filepath)
    g.image = f"gov_info/images/{filename}"
    g.save()
print(f"Successfully generated and assigned images for {schemes.count()} gov schemes.")

# 3. GENERATE NEWS IMAGES
print("\n--- Updating News Images ---")
news_articles = news.objects.all()
for n in news_articles:
    safe_name = "".join([c if c.isalnum() else "_" for c in n.title])[:30].strip("_")
    filename = f"news_{n.id}_{safe_name}.jpg"
    filepath = os.path.join(NEWS_DIR, filename)
    cat = categorize_title(n.category + " " + n.title)
    create_banner_image(n.title, n.category, cat, filepath)
    n.image = f"news/images/{filename}"
    n.save()
print(f"Successfully generated and assigned images for {news_articles.count()} news articles.")

print("\n--- Final Image Status Verification ---")
print("Blogs missing image:", bloag.objects.filter(image='').count() + bloag.objects.filter(image__isnull=True).count())
print("Gov schemes missing image:", gov_info.objects.filter(image='').count() + gov_info.objects.filter(image__isnull=True).count())
print("News missing image:", news.objects.filter(image='').count() + news.objects.filter(image__isnull=True).count())
