import os
import django
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'krushi_mitra.settings')
django.setup()

from farmer.models import crop
from django.db.models import Q

MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'crop', 'images')
os.makedirs(MEDIA_DIR, exist_ok=True)

# Color palettes (bg1, bg2, accent, label)
CROP_THEMES = {
    'bajra': {'bg1': (210, 180, 140), 'bg2': (160, 130, 90), 'accent': (120, 90, 50), 'label': 'Pearl Millet / Bajra'},
    'black gram': {'bg1': (70, 70, 70), 'bg2': (40, 40, 40), 'accent': (30, 30, 30), 'label': 'Black Gram (Urad)'},
    'castor': {'bg1': (180, 160, 120), 'bg2': (130, 110, 80), 'accent': (100, 80, 50), 'label': 'Castor Seed'},
    'chickpea': {'bg1': (230, 195, 140), 'bg2': (190, 150, 95), 'accent': (150, 110, 60), 'label': 'Chickpea (Chana)'},
    'coriander': {'bg1': (120, 180, 100), 'bg2': (70, 130, 60), 'accent': (40, 90, 30), 'label': 'Coriander (Dhaniya)'},
    'cotton': {'bg1': (240, 245, 250), 'bg2': (200, 215, 230), 'accent': (150, 175, 200), 'label': 'Raw Cotton'},
    'cumin': {'bg1': (190, 150, 110), 'bg2': (140, 100, 60), 'accent': (100, 65, 35), 'label': 'Cumin (Jeera)'},
    'green gram': {'bg1': (130, 190, 110), 'bg2': (75, 140, 60), 'accent': (45, 100, 35), 'label': 'Green Gram (Moong)'},
    'groundnut': {'bg1': (210, 165, 115), 'bg2': (165, 120, 75), 'accent': (125, 85, 45), 'label': 'Groundnut (Peanut)'},
    'maize': {'bg1': (245, 210, 90), 'bg2': (205, 160, 40), 'accent': (165, 120, 20), 'label': 'Maize (Corn)'},
    'mustard': {'bg1': (240, 215, 70), 'bg2': (190, 165, 30), 'accent': (140, 115, 15), 'label': 'Mustard (Sarson)'},
    'onion': {'bg1': (220, 130, 140), 'bg2': (160, 70, 80), 'accent': (120, 40, 50), 'label': 'Fresh Red Onion'},
    'potato': {'bg1': (200, 170, 130), 'bg2': (150, 120, 80), 'accent': (110, 80, 50), 'label': 'Fresh Potato'},
    'rice': {'bg1': (240, 240, 225), 'bg2': (205, 205, 180), 'accent': (160, 160, 130), 'label': 'Paddy Rice'},
    'soybean': {'bg1': (215, 195, 145), 'bg2': (175, 155, 105), 'accent': (135, 115, 65), 'label': 'Yellow Soybean'},
    'tomato': {'bg1': (235, 85, 75), 'bg2': (185, 45, 35), 'accent': (135, 25, 20), 'label': 'Farm Fresh Tomato'},
    'wheat': {'bg1': (235, 195, 110), 'bg2': (195, 145, 60), 'accent': (145, 100, 30), 'label': 'Golden Wheat Grain'},
}

def generate_crop_image(crop_key, filename):
    filepath = os.path.join(MEDIA_DIR, filename)
    theme = CROP_THEMES.get(crop_key.lower(), {
        'bg1': (180, 200, 160), 'bg2': (120, 150, 100),
        'accent': (80, 110, 60), 'label': crop_key.title()
    })
    
    width, height = 600, 400
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # Vertical gradient background
    bg1 = theme['bg1']
    bg2 = theme['bg2']
    for y in range(height):
        r = int(bg1[0] + (bg2[0] - bg1[0]) * y / height)
        g = int(bg1[1] + (bg2[1] - bg1[1]) * y / height)
        b = int(bg1[2] + (bg2[2] - bg1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Decorative shapes
    accent = theme['accent']
    draw.ellipse([width - 150, -50, width + 50, 150], fill=(*accent, 40))
    draw.ellipse([-50, height - 150, 150, height + 50], fill=(*accent, 40))
    
    # Inner border
    margin = 15
    draw.rectangle([margin, margin, width - margin, height - margin], outline=(255, 255, 255), width=3)
    
    # Central container card
    card_margin_x, card_margin_y = 60, 80
    draw.rectangle(
        [card_margin_x, card_margin_y, width - card_margin_x, height - card_margin_y],
        fill=(0, 0, 0),
        outline=(255, 255, 255),
        width=2
    )
    
    # Text rendering
    label = theme['label']
    try:
        font_large = ImageFont.truetype("arial.ttf", 32)
        font_sub = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font_large = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), label, font=font_large)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text(((width - text_w) / 2, (height - text_h) / 2 - 15), label, fill=(255, 255, 255), font=font_large)
    
    sub_text = "Krushi Mitra Farm Fresh"
    bbox_sub = draw.textbbox((0, 0), sub_text, font=font_sub)
    text_sub_w = bbox_sub[2] - bbox_sub[0]
    draw.text(((width - text_sub_w) / 2, (height - text_h) / 2 + 30), sub_text, fill=(240, 240, 200), font=font_sub)
    
    img.save(filepath, 'JPEG', quality=95)
    print(f"Generated image: {filename}")

EXISTING_IMAGE_MAP = {
    'alphonso mangoes': 'crop/images/Alphonso_Mangoes.jpg',
    'bt cotton': 'crop/images/BT_Cotton.jpg',
    'basmati rice (export quality)': 'crop/images/Basmati_Rice_Export_Quality.jpg',
    'fresh red tomatoes': 'crop/images/Fresh_Red_Tomatoes.jpg',
    'jeera (cumin seeds)': 'crop/images/Jeera_Cumin_Seeds.jpg',
    'organic sharbati wheat': 'crop/images/Organic_Sharbati_Wheat.jpg',
    'tur dal (pigeon pea)': 'crop/images/Tur_Dal_Pigeon_Pea.jpg',
    'black til': 'crop/images/black_til.jpg',
    'brocolli': 'crop/images/2721415.jpg',
}

NEW_CROP_FILES = {
    'bajra': 'bajra.jpg',
    'black gram': 'black_gram.jpg',
    'castor': 'castor.jpg',
    'chickpea': 'chickpea.jpg',
    'coriander': 'coriander.jpg',
    'cotton': 'cotton.jpg',
    'cumin': 'cumin.jpg',
    'green gram': 'green_gram.jpg',
    'groundnut': 'groundnut.jpg',
    'maize': 'maize.jpg',
    'mustard': 'mustard.jpg',
    'onion': 'onion.jpg',
    'potato': 'potato.jpg',
    'rice': 'rice.jpg',
    'soybean': 'soybean.jpg',
    'tomato': 'tomato.jpg',
    'wheat': 'wheat.jpg',
}

# 1. Generate missing image files
for crop_key, filename in NEW_CROP_FILES.items():
    generate_crop_image(crop_key, filename)

# 2. Update Database Records
all_crops = crop.objects.all()
updated_count = 0

for c in all_crops:
    name_lower = c.cropname.strip().lower()
    
    target_img_path = None
    
    if name_lower in EXISTING_IMAGE_MAP:
        target_img_path = EXISTING_IMAGE_MAP[name_lower]
    elif name_lower in NEW_CROP_FILES:
        target_img_path = f"crop/images/{NEW_CROP_FILES[name_lower]}"
    else:
        for key in NEW_CROP_FILES:
            if key in name_lower:
                target_img_path = f"crop/images/{NEW_CROP_FILES[key]}"
                break
    
    if target_img_path:
        c.image = target_img_path
        c.save()
        updated_count += 1

print(f"\nSuccessfully updated {updated_count} / {all_crops.count()} crops in database.")
missing_after = crop.objects.filter(Q(image='') | Q(image__isnull=True)).count()
print(f"Crops missing image after update: {missing_after}")
