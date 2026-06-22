from django.shortcuts import render
from farmer.models import *
from farmer.views import *
from models import *
# Create your views here.


@check_login(['Buyer'])
def buyer_home(request):
    all_crops = crop.objects.filter(is_approved = True)
    print("==================>",all_crops)
    context = {'all_crops' : all_crops}
    return render(request, "buyer/home.html",context)

@check_login(['Buyer'])
def buyer_bulk_order(request):
    return render(request, "buyer/bulk_order.html")

@check_login(['Buyer'])
def buyer_order_history(request):
    return render(request, "buyer/order_history.html")

@check_login(['Buyer'])
def buyer_profile(request):
    uid = request.uid
    print("=================>",uid)
    context = { 'uid' : uid }
    return render(request, "buyer/profile.html",context)

@check_login(['Buyer'])
def buyer_purchase_crop(request):
    return render(request, "buyer/purchase_crop.html")


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