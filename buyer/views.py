from requests import request
from django.shortcuts import render, redirect
from farmer.models import *
from farmer.views import *
from .models import *
# Create your views here.


@check_login(['Buyer'])
def buyer_home(request):
    all_crops = crop.objects.filter(is_approved = True)
    print("==================>",all_crops)
    context = {'all_crops' : all_crops}
    return render(request, "buyer/dashboard.html",context)

@check_login(['Buyer'])
def buyer_dashboard(request):
    return render(request, "buyer/dashboard.html")

@check_login(['Buyer'])
def buyer_browse_crops(request):
    all_crops = crop.objects.filter(is_approved = True)
    print("==================>",all_crops)
    context = {'all_crops' : all_crops}
    return render(request, "buyer/browse-crops.html",context)


@check_login(['Buyer'])
def buyer_crop_details(request,pk):
    return render(request, "buyer/crop-details.html")

@check_login(['Buyer'])
def buyer_cart(request):
    uid = request.uid
    cart = Cart.objects.get(user = uid)
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        context = {'cart_items':cart_items,'cart':cart}
        return render(request, "buyer/cart.html",context)
    else:
        cart = Cart.objects.create(user = uid)
        cart.save()
    return render(request, "buyer/cart.html")



@check_login(['Buyer'])
def cart_item_delete(request,pk):
    uid = request.uid
    cart = Cart.objects.get(user = uid)
    item = CartItem.objects.get(id = pk)
    item.delete()
    cart_items = CartItem.objects.filter(cart=cart)
    context = {'cart_items':cart_items,'cart':cart}
    return redirect('buyer_cart')



@check_login(['Buyer'])
def buyer_orders(request):
    return render(request, "buyer/orders.html")

@check_login(['Buyer'])
def buyer_wishlist(request):
    return render(request, "buyer/wishlist.html")

@check_login(['Buyer'])
def buyer_bulk_order(request):
    return render(request, "buyer/bulk-order.html")

@check_login(['Buyer'])
def buyer_export_inquiry(request):
    return render(request, "buyer/export-inquiry.html")

@check_login(['Buyer'])
def buyer_messages(request):
    return render(request, "buyer/messages.html")

@check_login(['Buyer'])
def buyer_notifications(request):
    return render(request, "buyer/notifications.html")

@check_login(['Buyer'])
def buyer_profile(request):
    uid = getattr(request, 'uid', None)
    context = { 'uid' : uid } if uid else {}
    return render(request, "buyer/profile.html", context)

@check_login(['Buyer'])
def buyer_verification(request):
    return render(request, "buyer/verification.html")

@check_login(['Buyer'])
def buyer_bank_details(request):
    return render(request, "buyer/bank-details.html")

@check_login(['Buyer'])
def buyer_settings(request):
    return render(request, "buyer/settings.html")

@check_login(['Buyer'])
def buyer_checkout(request):
    return render(request, "buyer/checkout.html")


@check_login(['Buyer'])
def buyer_order_details(request):
    return render(request, "buyer/order-details.html")

@check_login(['Buyer'])
def kyc(request):
    user = getattr(request, 'uid', request.user)
    try:
        buyer = Buyer.objects.get(user=user)
    except Buyer.DoesNotExist:
        buyer = Buyer(user=user)
        
    if request.method == 'POST':
        buyer.adharno = request.POST.get('adharno', buyer.adharno)
        buyer.pan_no = request.POST.get('pan_no', buyer.pan_no)
        buyer.gst_no = request.POST.get('gst_no', buyer.gst_no)
        buyer.msme_no = request.POST.get('msme_no', buyer.msme_no)
        buyer.trade_license = request.POST.get('trade_license', buyer.trade_license)
        buyer.business_type = request.POST.get('business_type', buyer.business_type)
        buyer.account_no = request.POST.get('account_no', buyer.account_no)
        buyer.ifsc_code = request.POST.get('ifsc_code', buyer.ifsc_code)
        buyer.bank_name = request.POST.get('bank_name', buyer.bank_name)
        buyer.account_holder = request.POST.get('account_holder', buyer.account_holder)
        buyer.address = request.POST.get('address', buyer.address)
        
        if 'adharcard' in request.FILES:
            buyer.adharcard = request.FILES['adharcard']
        if 'pancard' in request.FILES:
            buyer.pancard = request.FILES['pancard']
        if 'gst_certificate' in request.FILES:
            buyer.gst_certificate = request.FILES['gst_certificate']
        if 'seventwel' in request.FILES:
            buyer.seventwel = request.FILES['seventwel']
        if 'passbook' in request.FILES:
            buyer.passbook = request.FILES['passbook']
        if 'trade_license_doc' in request.FILES:
            buyer.trade_license_doc = request.FILES['trade_license_doc']
        if 'photo' in request.FILES:
            buyer.photo = request.FILES['photo']
            
        buyer.save()
        messages.success(request, 'KYC details submitted successfully!')
        return redirect('kyc')
        
    return render(request, "buyer/kyc.html", {'buyer': buyer})

def home(request):
    return HttpResponse("Welcome to Krushi Mitra! You are logged in.")  