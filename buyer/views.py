import buyer
import buyer
import buyer
import string , json
from django.template import context
from requests import request
from django.shortcuts import render, redirect
from farmer.models import *
from farmer.views import *
from .models import *
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.



@check_login(['Buyer'])
def buyer_home(request):
    return redirect("buyer_dashboard")

def premium_required(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            buyer = Buyer.objects.get(user=request.uid)
        except Buyer.DoesNotExist:
            messages.error(request, "Only buyers can access this page.")
            return redirect("login")   # ya home page

        premium = premium_buyer.objects.filter(user=buyer).first()

        if not premium or premium.premium_type == "Free" or premium.is_expired:
            messages.error(request, "This feature is available for Premium users only.")
            return redirect("buyer_premium")

        return view_func(request, *args, **kwargs)

    return wrapper

def format_indian_number(value):
    value = float(value)

    if value >= 10000000:  # 1 Crore
        return f"{value / 10000000:.2f} Cr"
    elif value >= 100000:  # 1 Lakh
        return f"{value / 100000:.2f} Lakh"
    elif value >= 1000:  # 1 Thousand
        return f"{value / 1000:.2f} K"
    else:
        return f"{value:.2f}"

def chek_premium(buyr):
    premium_buyr = premium_buyer.objects.filter(user=buyr).first()

    if not premium_buyr:
        premium_buyr = premium_buyer.objects.create(
            user=buyr,
            premium_type="Free",
            premium_time="Monthly"
        )

    premium_buyr.check_subscription()
    return premium_buyr
    
@check_login(['Buyer'])
def buyer_dashboard(request):
    uid = request.uid
    orders = Order.objects.filter(user = uid).order_by('-id')
    items = OrderItem.objects.filter(order__in=orders).order_by('-id')[:6]
    item_count = OrderItem.objects.filter(order__in=orders).count()
    pending_count = OrderItem.objects.filter(order__in=orders, order__status='Pending').count()    
    complated = OrderItem.objects.filter(order__in=orders, order__status='Delivered').count()
    buyr = Buyer.objects.get(user=uid)
    cart = Cart.objects.get(user = uid)
    premium_buyr = chek_premium(buyr)
    premium_type = premium_buyer.objects.get(user=buyr)
    if premium_type.premium_type == "Free":
        buyr.is_premiume = False
        buyr.save()
        cart.cart_limit = 1000
        cart.save()
    else:
        buyr.is_premiume = True
        buyr.save()
    total_value = 0
    for order in orders:
        total_value+= order.total_amount
    formatted_total = format_indian_number(total_value)

    all_crops = crop.objects.filter(is_approved = True)

    context = {'buyr':buyr,'premium_type':premium_type,'all_crops' : all_crops,'items':items,'total_value':total_value,
    'formatted_total':formatted_total,'item_count':item_count,'pending_count':pending_count,'complated':complated}
    return render(request, "buyer/dashboard.html",context)

@check_login(['Buyer'])
def buyer_browse_crops(request):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    cart = Cart.objects.get(user = uid)
    all_crops = crop.objects.filter(is_approved = True)
    saved_crops = saved.objects.filter( user=buyr).values_list('crop_id', flat=True)
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    print("==================>",all_crops)
    context = {'all_crops' : all_crops,"saved_crops":saved_crops,'premium_type':premium_type,'buyr':buyr,'cart':cart}
    return render(request, "buyer/browse-crops.html",context)


@check_login(['Buyer'])
def buyer_crop_details(request,pk):
    uid = request.uid
    crp = crop.objects.get(id=pk)
    cart = Cart.objects.get(user = uid)
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    context = {'crop' : crp,'premium_type':premium_type,'buyr':buyr,'cart':cart}
    return render(request, "buyer/crop-details.html",context)

@check_login(['Buyer'])
def buyer_cart(request):
    uid = request.uid
    cart = Cart.objects.get(user = uid)
    buyr = Buyer.objects.get(user=uid)
    cart_items = CartItem.objects.filter(cart=cart)
    total_qty = 0
    if cart_items:
        total_qty = [total_qty+(itme.quantity * 20) for itme in cart_items]
        total_qty = total_qty[0]
    premium_type = premium_buyer.objects.get(user=buyr)
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        crop_id = request.POST.get('crop')
        crop_obj = crop.objects.get(id=crop_id)

        cart_item = CartItem.objects.filter(cart=cart,crop=crop_obj).first()

        if cart_item:
            cart_item.quantity+= int(quantity)
            cart_item.save()
            cart_items = CartItem.objects.filter(cart=cart)
            context = {'cart_items':cart_items,'cart':cart,'premium_type':premium_type,'buyr':buyr,'total_qty':total_qty}
            return render(request, "buyer/cart.html",context)
        else:
            cart_item = CartItem.objects.create(cart=cart,crop=crop_obj,quantity=quantity)
            cart_item.save()    
            cart_items = CartItem.objects.filter(cart=cart)
            context = {'cart_items':cart_items,'cart':cart,'premium_type':premium_type,'total_qty':total_qty}
            return render(request, "buyer/cart.html",context)
        
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        context = {'cart_items':cart_items,'cart':cart,'premium_type':premium_type,'total_qty':total_qty}
        return render(request, "buyer/cart.html",context)
    else:
        cart = Cart.objects.create(user = uid)
        cart.save()
    return render(request, "buyer/cart.html")

@check_login(['Buyer'])
def buyer_addto_cart(request):
    uid = request.uid
    cart = Cart.objects.get(user = uid)
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        crop_id = request.POST.get('crop')
        crop_obj = crop.objects.get(id=crop_id)

        cart_item = CartItem.objects.filter(cart=cart,crop=crop_obj).first()

        if cart_item:
            cart_item.quantity+= int(quantity)
            cart_item.save()
            return redirect('buyer_browse_crops')
        else:
            cart_item = CartItem.objects.create(cart=cart,crop=crop_obj,quantity=quantity)
            cart_item.save()    
            return redirect('buyer_browse_crops')

@check_login(['Buyer'])
def cart_item_delete(request,pk):
    uid = request.uid
    cart = Cart.objects.get(user = uid)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        crop_id = request.POST.get('crop')
        crop_obj = crop.objects.get(id=crop_id)
        cart_item = CartItem.objects.filter(cart=cart,crop=crop_obj).first() 
        cart_item.quantity = quantity
        cart_item.save()
        cart_items = CartItem.objects.filter(cart=cart)
        return redirect('buyer_cart')
    else:
        item = CartItem.objects.get(id = pk)
        item.delete()
        cart_items = CartItem.objects.filter(cart=cart)
        return redirect('buyer_cart')

@check_login(['Buyer'])
def buyer_checkout(request):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    cart = Cart.objects.get(user = uid)
    cart_items = CartItem.objects.filter(cart=cart)
    premium_type = premium_buyer.objects.get(user=buyr)
    total_quantity = 0
    quantity_limit = cart.cart_limit
    if request.method == 'POST':
        payment_method = request.POST.get('payment')
        con_order = Order.objects.create(
             user = uid,
             subtotal = cart.total_price,
             tax = cart.tax,
             total_amount = cart.final_price,
             payment_method = payment_method
        )
        con_order.save()

        for item in cart_items:
            order_item = OrderItem.objects.create(
                order = con_order,
                crop = item.crop ,
                crop_name = item.crop.cropname,
                price = item.crop.price,
                quantity = item.quantity,
                subtotal = item.subtotal
            )
            total_quantity += (item.quantity * 20)
        cart_items.delete()
        cart.total_kg += total_quantity
        cart.save()
        notification = notifications.objects.create(
            user = buyr,
            notification_type = "Payment",
            message = f"Payment of ₹{con_order.total_amount} for order {con_order.order_id} confirmed."
        )
        return redirect("buyer_dashboard")

    context = {"uid":uid,"cart":cart,"cart_items":cart_items ,'buyr':buyr,'premium_type':premium_type,'buyr':buyr}
    return render(request, "buyer/checkout.html",context)

@check_login(['Buyer'])
def buyer_orders(request):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    order = Order.objects.filter(user = uid)
    items = OrderItem.objects.filter(order__in=order)
    total_order = len(items)
    pending_order = len([item for item in items if item.order.status=="Pending"])
    confirmed_order = len([item for item in items if item.order.status=="Confirmed"])
    shipped_order = len([item for item in items if item.order.status=="Shipped"])
    delivered_order = len([item for item in items if item.order.status=="Delivered"])
    cancelled_order = len([item for item in items if item.order.status=="Cancelled"])

    context = {'uid':uid,'buyr':buyr,'order':order,'items':items,
                'total_order':total_order,'pending_order':pending_order,
                'shipped_order':shipped_order,'delivered_order':delivered_order,
                'cancelled_order':cancelled_order,'premium_type':premium_type,'buyr':buyr
                }
    return render(request, "buyer/orders.html",context)

@check_login(['Buyer'])
def buyer_order_details(request,pk):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    item = OrderItem.objects.get(id=pk)
    context = {'uid':uid,'buyr':buyr,'item':item,'premium_type':premium_type,'buyr':buyr}
    return render(request, "buyer/order-details.html",context)

@check_login(['Buyer'])
def buyer_wishlist(request):    
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    saved_crops = saved.objects.filter(user=buyr)
    total_saved = len(saved_crops)
    context={'saved_crops':saved_crops,'total_saved':total_saved,'uid':uid,'premium_type':premium_type,'buyr':buyr}
    return render(request, "buyer/wishlist.html",context)

@check_login(['Buyer'])
def add_wishlist(request,pk): 
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    crop_ = crop.objects.get(id=pk)
    if request.method == 'POST':
        saved_crop = saved.objects.filter(user=buyr)
        if saved_crop:
            saved_crop.delete()
            return redirect('buyer_wishlist')
        else: 
            return redirect('buyer_wishlist')
    else:
        saved_crop = saved.objects.filter(user=buyr, crop=crop_).first()
        if saved_crop:
            saved_crop.delete()
        else:
            save_crop = saved.objects.create(user=buyr,crop=crop_)
        return redirect('buyer_wishlist')


@check_login(['Buyer'])
@premium_required
def buyer_bulk_order(request):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    
    if request.method == 'POST':
        crop_name = request.POST.get('crop_name')
        category = request.POST.get('category')
        required_quantity = request.POST.get('required_quantity')
        unit = request.POST.get('unit')
        target_price = request.POST.get('target_price')
        required_date = request.POST.get('required_date')
        delivery_state = request.POST.get('delivery_state')
        delivery_district = request.POST.get('delivery_district')
        additional_notes = request.POST.get('additional_notes')
        
        bulkrequest.objects.create(
            user=buyr,
            crop_name=crop_name,
            category=category,
            required_quantity=required_quantity,
            unit=unit,
            target_price=target_price,
            required_date=required_date,
            delivery_state=delivery_state,
            delivery_district=delivery_district,
            additional_notes=additional_notes
        )
        messages.success(request, 'Bulk order request submitted successfully!')
        return redirect('buyer_bulk_order')
        
    inquiries = bulkrequest.objects.filter(user=buyr).order_by('-created_at')
    return render(request, "buyer/bulk-order.html", {'premium_type': premium_type, 'buyr': buyr, 'inquiries': inquiries})

@check_login(['Buyer'])
@premium_required
def buyer_export_inquiry(request):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    
    if request.method == 'POST':
        country = request.POST.get('country')
        crop_name = request.POST.get('crop_name')
        required_quantity = request.POST.get('required_quantity')
        packaging_type = request.POST.get('packaging_type')
        quality_standard = request.POST.get('quality_standard')
        shipping_port = request.POST.get('shipping_port')
        expected_price = request.POST.get('expected_price')
        expected_delivery = request.POST.get('expected_delivery')
        additional_notes = request.POST.get('additional_notes')
        
        exportinquiry.objects.create(
            user=buyr,
            country=country,
            crop_name=crop_name,
            required_quantity=required_quantity,
            packaging_type=packaging_type,
            quality_standard=quality_standard,
            shipping_port=shipping_port,
            expected_price=expected_price,
            expected_delivery=expected_delivery,
            additional_notes=additional_notes
        )
        messages.success(request, 'Export inquiry submitted successfully!')
        return redirect('buyer_export_inquiry')
        
    inquiries = exportinquiry.objects.filter(user=buyr).order_by('-created_at')
    return render(request, "buyer/export-inquiry.html", {'premium_type': premium_type, 'buyr': buyr, 'inquiries': inquiries})

@check_login(['Buyer'])
def buyer_messages(request):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    num = 33
    return render(request, "buyer/messages.html",{'num':num,'premium_type':premium_type,'buyr':buyr})

@check_login(['Buyer'])
def buyer_notifications(request):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    all_notifications = notifications.objects.filter(user=buyr)
    context={'buyr':buyr,'all_notifications':all_notifications,'premium_type':premium_type,'buyr':buyr}
    return render(request, "buyer/notifications.html",context)

@check_login(['Buyer'])
def buyer_profile(request):
    uid = getattr(request, 'uid', None)
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    bank_info = bank_details.objects.filter(user=buyr).first()
    verification = verification_details.objects.filter(user=buyr).first()
    context = { 'uid' : uid,'premium_type':premium_type,'buyr':buyr, 'bank_info': bank_info, 'verification': verification } if uid else {}
    return render(request, "buyer/profile.html", context)

@check_login(['Buyer'])
def buyer_verification(request):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    verification = verification_details.objects.filter(user=buyr).first()

    if request.method == 'POST':
        if not buyr.enable_update:
            messages.error(request, 'You cannot change verification data as updates are disabled.')
            return redirect('buyer_verification')
        if not verification:
            verification = verification_details(user=buyr)
        
        buyr.gst_no = request.POST.get('gst_no', buyr.gst_no)
        if 'gst_certificate' in request.FILES:
            buyr.gst_certificate = request.FILES['gst_certificate']
        buyr.save()

        verification.msme_no = request.POST.get('msme_no', verification.msme_no)
        verification.trade_license = request.POST.get('trade_license', verification.trade_license)
        verification.adharno = request.POST.get('adharno', verification.adharno)
        
        if 'photo' in request.FILES:
            verification.photo = request.FILES['photo']
        if 'trade_license_doc' in request.FILES:
            verification.trade_license_doc = request.FILES['trade_license_doc']
        if 'adharcard' in request.FILES:
            verification.adharcard = request.FILES['adharcard']
            
        verification.save()
        messages.success(request, 'Verification details updated successfully!')
        return redirect('buyer_verification')

    return render(request, "buyer/verification.html",{'premium_type':premium_type,'buyr':buyr, 'verification': verification})

@check_login(['Buyer'])
def buyer_bank_details(request):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    bank_info = bank_details.objects.filter(user=buyr).first()

    if request.method == 'POST':
        if not buyr.enable_update:
            messages.error(request, 'You cannot change bank details as updates are disabled.')
            return redirect('buyer_bank_details')
        if not bank_info:
            bank_info = bank_details(user=buyr)
            
        bank_info.pan_no = request.POST.get('pan_no', bank_info.pan_no)
        bank_info.account_holder = request.POST.get('account_holder', bank_info.account_holder)
        bank_info.account_no = request.POST.get('account_no', bank_info.account_no)
        bank_info.ifsc_code = request.POST.get('ifsc_code', bank_info.ifsc_code)
        bank_info.bank_name = request.POST.get('bank_name', bank_info.bank_name)

        if 'pancard' in request.FILES:
            bank_info.pancard = request.FILES['pancard']
        if 'passbook' in request.FILES:
            bank_info.passbook = request.FILES['passbook']
            
        bank_info.save()
        messages.success(request, 'Bank details updated successfully!')
        return redirect('buyer_bank_details')

    return render(request, "buyer/bank-details.html",{'premium_type':premium_type,'buyr':buyr, 'bank_info': bank_info})

@check_login(['Buyer'])
def buyer_settings(request):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    return render(request, "buyer/settings.html",{'premium_type':premium_type,'buyr':buyr})

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

@check_login(['Buyer'])
def buyer_premium(request):
    uid = request.uid
    plans = premium_plans.objects.get()
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    coupons = premium_coupon.objects.filter(is_active=True).values('code','discount_type','discount_value','label')
    coupon_data = {
    c["code"]: {
        "type": c["discount_type"],
        "value": float(c["discount_value"]),
        "label": c["label"],
    }
    for c in coupons
    }
    print("=====================>",coupon_data)
    if request.method == 'POST':
        plan = request.POST.get('plan')
        return render(request, "buyer/premiumcheckout.html", {'uid': uid ,'plans':plans,'buyr':buyr,'premium_type':premium_type,'plan':plan, 'coupons': json.dumps(coupon_data),})
    return render(request, "buyer/premium.html", {'uid': uid ,'plans':plans,'buyr':buyr,'premium_type':premium_type})

@check_login(['Buyer'])
def premium_checkout(request):
    uid = request.uid
    plans = premium_plans.objects.get()
    buyr = Buyer.objects.get(user=uid)
    alrady_premium = premium_buyer.objects.get(user=buyr)
    coupons = premium_coupon.objects.filter(is_active=True).values('code','discount_type','discount_value','label')
    coupon_data = {
    c["code"]: {
        "type": c["discount_type"],
        "value": c["discount_value"],
        "label": c["label"],
    }
    for c in coupons
    }
    print("=====================>",coupon_data)

    if request.method == 'POST':
        plan = request.POST.get('plan')
        total = request.POST.get('total')
        billing_cycle = request.POST.get('billing_cycle')
        billing_cycle = billing_cycle.capitalize()
        payment_method = request.POST.get('payment_method')
        coupon_code = request.POST.get('coupon_code')
        cart = Cart.objects.get(user = uid)
        print("++++++++++++++++++++++++}",plan ,total,billing_cycle,payment_method,coupon_code)
        
        if not plan or not billing_cycle:
            messages.error(request, "Invalid checkout data. Please select a plan again.")
            return redirect('buyer_premium')
            
        if alrady_premium:
            alrady_premium.premium_type = plan
            alrady_premium.premium_time = billing_cycle
            alrady_premium.purchase_date = timezone.now()
            alrady_premium.save()
            cart.cart_limit = 5000
            cart.save()

            buy_premium_his = premium_history.objects.create(
                user = buyr,
                plan = plan,
                billing_cycle = billing_cycle,
                payment_method = payment_method,
                price = total,
                coupon_code = coupon_code,
                start_date =  timezone.now()
            )
            buy_premium_his.save()
        
        else:
            buy_premium = premium_buyer.objects.create(
                user=buyr,
                premium_type=plan,
                premium_time=billing_cycle,
                purchase_date = timezone.now()
            )
            buy_premium_his = premium_history.objects.create(
                user = buyr,
                plan = plan,
                billing_cycle = billing_cycle,
                payment_method = payment_method,
                price = total,
                coupon_code = coupon_code,
                start_date =  timezone.now()
            )
            buy_premium_his.save()

            cart.cart_limit = 5000
            cart.save()
            buyr.is_premiume = True
            buyr.save()
        notification = notifications.objects.create(
        user = buyr,
        notification_type = "Premium",
        message = f"You buy {plan} plan at ₹{total} in {billing_cycle} term.")
        notification.save()
        return redirect('buyer_dashboard')
    return render(request, "buyer/premiumcheckout.html", {'uid': uid ,'plans':plans,'buyr':buyr,'premium_type':alrady_premium, "coupons": json.dumps(list(coupon_data))})

@check_login(['Buyer'])
def current_plan(request):
    uid = request.uid
    buyr = Buyer.objects.get(user=uid)
    premium_type = premium_buyer.objects.get(user=buyr)
    cart = Cart.objects.get(user=uid)
    cart_used = cart.total_kg
    cart_limit = cart.cart_limit
    cart_usage_pct = min(int((cart_used / cart_limit) * 100), 100)
    last_buy = premium_history.objects.filter(user=buyr).first()
    return render(request, "buyer/current_plan.html", {
        'buyr': buyr,
        'premium_type': premium_type,
        'cart': cart,
        'cart_used': cart_used,
        'cart_usage_pct': cart_usage_pct,
        'last_buy':last_buy
    })
