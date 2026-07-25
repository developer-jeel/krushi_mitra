import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'krushi_mitra.settings')
django.setup()

from farmer.models import crop

crops_to_update = crop.objects.filter(price__lt=500)
count = crops_to_update.count()
print(f"Found {count} crops with price < 500 (per 1kg prices).")

for c in crops_to_update:
    c.price = c.price * 20
    c.save()

print(f"Successfully converted {count} crop prices to 20kg total!")
print("New min price:", crop.objects.all().aggregate(django.db.models.Min('price'))['price__min'])
print("New max price:", crop.objects.all().aggregate(django.db.models.Max('price'))['price__max'])
print("Sample converted prices:", [(c.id, c.cropname, c.price) for c in crop.objects.all()[:15]])
