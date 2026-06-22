from django.db import models
from farmer.models import *

# Create your models here.

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