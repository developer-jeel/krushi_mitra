from django.db import models
from farmer.models import *
from django.utils.html import mark_safe
from django.utils import timezone


# Create your models here.

class Buyer(models.Model):
    STATE_CHOICES = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer')
    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=100,choices=STATE_CHOICES,default='Gujarat')
    pincode = models.CharField(max_length=6,blank=True, null=True)
    business_type = models.CharField(max_length=50, blank=True, null=True)
    gst_certificate = models.FileField(upload_to='buyer/documents/gst/', blank=True, null=True)
    gst_no = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    enable_update = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Buyer: {self.user.name}"

class bank_details(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='buyer_bank')
    pan_no = models.CharField(max_length=20, blank=True, null=True)
    pancard = models.FileField(upload_to='buyer/documents/pancard/', blank=True, null=True)
    passbook = models.FileField(upload_to='buyer/documents/passbook/', blank=True, null=True)
    account_holder = models.CharField(max_length=100, blank=True, null=True)
    account_no = models.CharField(max_length=30, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Buyer: {self.user.user.name}"

class verification_details(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='buyer_details')
    photo = models.ImageField(upload_to='buyer/profile_photos/', blank=True, null=True)
    msme_no = models.CharField(max_length=50, blank=True, null=True)
    trade_license = models.CharField(max_length=50, blank=True, null=True)
    trade_license_doc = models.FileField(upload_to='buyer/documents/trade_license/', blank=True, null=True)
    adharno = models.CharField(max_length=20, unique=True, blank=True, null=True)
    adharcard = models.FileField(upload_to='buyer/documents/adharcard/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def image_preview(self):
        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" width="40" style="border-radius:8px;"/>')
        return "—"
    image_preview.short_description = "Icon"

    def __str__(self):
        return self.user.user.name

    class Meta:
        ordering = ['-created_at']

class premium_buyer(models.Model):
    PREMIUM_CHOOSE =  (
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
    )
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='Premium_user')

class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    tax_per = models.IntegerField(blank=True, null=True,default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def tax(self):
        return (self.total_price * self.tax_per) / 100

    @property
    def final_price(self):
        return self.total_price + self.tax

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    crop = models.ForeignKey(crop,on_delete=models.CASCADE,related_name='crop')
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'crop')

    def __str__(self):
        return f"{self.crop.cropname} ------------------- >({self.quantity})"

    @property
    def subtotal(self):
        return self.crop.price * self.quantity



class Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    order_id = models.CharField(max_length=20,unique=True,blank=True)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    tax = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Pending')
    payment_method = models.CharField(max_length=50,blank=True,null=True)
    payment_status = models.CharField(max_length=20,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            count = Order.objects.count() + 1
            self.order_id = f"#ORD-{timezone.now().year}-{count:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    crop = models.ForeignKey(crop,on_delete=models.SET_NULL,null=True)
    crop_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return self.crop_name

class notifications(models.Model):
    NOTIFICATIONS_TYPES= ( 
        ("Order","Order"),
        ("Payment","Payment"),
        ("Bulk","Bulk"),
        ("Export","Export"),
        ("Kyc","Kyc"),
                            )
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='buyer')
    notification_type = models.CharField(max_length=20,choices=NOTIFICATIONS_TYPES)
    message = models.CharField(max_length=100,blank=True,null=True)
    is_readed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user} : {self.notification_type}"

class saved(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='saved_by')
    crop = models.ForeignKey(crop,on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.name} added {self.crop.cropname} in wishlist"