from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Farmer', 'Farmer'),
        ('Buyer', 'Buyer'),
        ('Subadmin', 'Subadmin')
    )
    
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True,blank=True, null=True)
    contact = models.CharField(max_length=10, unique=True , blank=True, null=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        if self.email:
            return self.email
        elif self.contact:
            return self.contact
        return "No Data"

class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer')
    farm_name = models.CharField(max_length=255 ,blank=True, null=True)
    acres = models.IntegerField(blank=True, null=True)
    address = models.TextField()
    adharno = models.CharField(max_length=20, unique=True, blank=True, null=True)
    adharcard = models.FileField(upload_to='farmer/documents/adharcard/', blank=True, null=True)
    pancard = models.FileField(upload_to='farmer/documents/pancard/', blank=True, null=True)
    passbook = models.FileField(upload_to='farmer/documents/passbook/', blank=True, null=True)
    seventwel = models.FileField(upload_to='farmer/documents/7_12/', blank=True, null=True)
    photo = models.ImageField(upload_to='farmer/profile_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"farmer : {self.user.name}"

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer')
    address = models.TextField(blank=True, null=True)
    pan_no = models.CharField(max_length=20, blank=True, null=True)
    msme_no = models.CharField(max_length=50, blank=True, null=True)
    trade_license = models.CharField(max_length=50, blank=True, null=True)
    business_type = models.CharField(max_length=50, blank=True, null=True)
    account_no = models.CharField(max_length=30, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_holder = models.CharField(max_length=100, blank=True, null=True)
    gst_certificate = models.FileField(upload_to='buyer/documents/gst/', blank=True, null=True)
    trade_license_doc = models.FileField(upload_to='buyer/documents/trade_license/', blank=True, null=True)
    gst_no = models.CharField(max_length=15, unique=True, blank=True, null=True)
    adharno = models.CharField(max_length=20, unique=True, blank=True, null=True)
    adharcard = models.FileField(upload_to='buyer/documents/adharcard/', blank=True, null=True)
    pancard = models.FileField(upload_to='buyer/documents/pancard/', blank=True, null=True)
    passbook = models.FileField(upload_to='buyer/documents/passbook/', blank=True, null=True)
    photo = models.ImageField(upload_to='buyer/profile_photos/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Buyer: {self.user.name}"

class chatroom(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_chat')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatRoom - {self.user.name}"

class message(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('ai', 'Ai'),
    )

    chat_room = models.ForeignKey(chatroom, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES) 
    content = models.TextField()
    image = models.FileField(upload_to='chat/images/', null=True, blank=True)
    video = models.FileField(upload_to='chat/videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} - {self.chat_room.user.name}"

class bloag(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='posted_by')
    title = models.CharField(max_length=20, unique=True, blank=True, null=True)
    content = models.TextField()
    image = models.FileField(upload_to='bloag/images/', null=True, blank=True)
    video = models.FileField(upload_to='bloag/videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} --> {self.title}"

class crop(models.Model):
    CATEGORY_CHOICES = (
        ('grain cereals', 'Grain cereals'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('pulses', 'Pulses'),
        ('spices', 'Spices'),
        ('cotton', 'Cotton'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="seller")
    cropname = models.CharField(max_length=20)
    category = models.CharField(max_length=20 , choices = CATEGORY_CHOICES)
    quantity = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='crop/images/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} --> {self.cropname}"

class community_message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="message_my")
    message = models.TextField()
    image = models.FileField(upload_to='community/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} --> {self.message}"

class gov_info(models.Model):
    STATE_CHOICES = [
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh", "Arunachal Pradesh"),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("Uttarakhand", "Uttarakhand"),
    ("West Bengal", "West Bengal"),
    ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"),
    ("Chandigarh", "Chandigarh"),
    ("Dadra and Nagar Haveli and Daman and Diu", "Dadra and Nagar Haveli and Daman and Diu"),
    ("Delhi", "Delhi"),
    ("Jammu and Kashmir", "Jammu and Kashmir"),
    ("Ladakh", "Ladakh"),
    ("Lakshadweep", "Lakshadweep"),
    ("Puducherry", "Puducherry"),
]
    title = models.CharField(max_length=255)
    description = models.TextField()
    oneline_info = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=100,choices=STATE_CHOICES)
    image = models.FileField(upload_to='gov_info/images/', null=True, blank=True)
    source_link = models.URLField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title