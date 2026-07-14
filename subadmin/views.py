from django.shortcuts import render
import random

def login(request):
    return render(request, "subadmin/login.html")

def dashboard(request):
    return render(request, "subadmin/dashboard.html")

def kyc_approval(request):
    return render(request, "subadmin/kyc_approval.html")

def manage_buyers(request):
    return render(request, "subadmin/manage_buyers.html")

def manage_farmers(request):
    return render(request, "subadmin/manage_farmers.html")

def order_management(request):
    return render(request, "subadmin/order_management.html")

def product_approval(request):
    return render(request, "subadmin/product_approval.html")

def profile(request):
    return render(request, "subadmin/profile.html")

def reports(request):
    return render(request, "subadmin/reports.html")

def support_tickets(request):
    return render(request, "subadmin/support_tickets.html")

def system_settings(request):
    return render(request, "subadmin/system_settings.html")
