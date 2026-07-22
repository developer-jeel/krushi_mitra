import csv
import json
from functools import wraps

from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from farmer.models import User, Farmer, crop, FarmerTool, bloag, community_message, news, gov_info, premium_buyer as farmer_premium_buyer
from buyer.models import (
    Buyer, Order, OrderItem, premium_buyer, verification_details,
    premium_coupon, discount_coupon, premium_history, premium_plans,
)
from buyer.views import format_indian_number


#format_indian_number
# ─────────────────────────────────────────────────────────────────────────────
# Auth helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_subadmin_user(request):
    contact = request.session.get('contact')
    if not contact:
        return None
    try:
        return User.objects.get(contact=contact, role='Subadmin', is_active=True)
    except User.DoesNotExist:
        return None


def check_subadmin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_subadmin_user(request)
        if not user:
            messages.error(request, 'Please log in to access the admin panel.')
            return redirect('subadmin:login')
        request.admin_user = user
        return view_func(request, *args, **kwargs)
    return wrapper


# ─────────────────────────────────────────────────────────────────────────────
# Login / Logout
# ─────────────────────────────────────────────────────────────────────────────

def login(request):
    if get_subadmin_user(request):
        return redirect('subadmin:dashboard')

    if request.method == 'POST':
        contact = request.POST.get('contact', '').strip()
        password = request.POST.get('password', '')
        try:
            user = User.objects.get(contact=contact, role='Subadmin')
            from django.contrib.auth.hashers import check_password
            if check_password(password, user.password):
                if not user.is_active:
                    messages.error(request, 'Your account is inactive. Contact super admin.')
                    return render(request, 'subadmin/login.html')
                request.session['contact'] = contact
                request.session['role'] = 'Subadmin'
                messages.success(request, f'Welcome back, {user.name}!')
                return redirect('subadmin:dashboard')
            else:
                messages.error(request, 'Invalid contact or password.')
        except User.DoesNotExist:
            messages.error(request, 'No admin account found with this contact.')
    return render(request, 'subadmin/login.html')


def logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('subadmin:login')


# ─────────────────────────────────────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def dashboard(request):
    # Core stats
    total_farmers   = Farmer.objects.count()
    total_buyers    = Buyer.objects.count()
    total_crops     = crop.objects.count()
    total_tools     = FarmerTool.objects.count()
    total_blogs     = bloag.objects.count()
    total_community = community_message.objects.count()
    total_orders    = Order.objects.count()
    total_news      = news.objects.count()
    pending_crops   = crop.objects.filter(is_approved=False).count()
    active_users    = User.objects.filter(is_active=True).count()
    total_revenue   = OrderItem.objects.aggregate(s=Sum('subtotal'))['s'] or 0
    total_revenue   = "" + format_indian_number(total_revenue)
    premium_buyers  = Buyer.objects.filter(is_premiume=True).count()

    # Pending KYC
    pending_kyc = Farmer.objects.filter(
        Q(adharcard='') | Q(adharcard__isnull=True)
    ).count()

    # Recent orders (last 5)
    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]

    # Chart data: monthly orders (last 12 months)
    from datetime import datetime, timedelta
    monthly_order_data = []
    monthly_labels = []
    now = timezone.now()
    for i in range(11, -1, -1):
        dt = now - timedelta(days=i * 30)
        count = Order.objects.filter(
            created_at__year=dt.year,
            created_at__month=dt.month
        ).count()
        monthly_order_data.append(count)
        monthly_labels.append(dt.strftime('%b'))

    # Crop category breakdown
    crop_categories = list(crop.objects.values('category').annotate(c=Count('id')).order_by('-c')[:6])

    # Recent registrations
    recent_users = User.objects.filter(role__in=['Farmer', 'Buyer']).order_by('-date_joined')[:8]

    # ── Coupon stats ──────────────────────────────────────────────────────────
    prem_total   = premium_coupon.objects.count()
    prem_active  = premium_coupon.objects.filter(is_active=True).count()
    prem_expired = premium_coupon.objects.filter(expiry_date__lt=now).count()
    prem_used    = premium_coupon.objects.aggregate(s=Sum('used_count'))['s'] or 0

    disc_total   = discount_coupon.objects.count()
    disc_active  = discount_coupon.objects.filter(is_active=True).count()
    disc_expired = discount_coupon.objects.filter(expiry_date__lt=now).count()
    disc_used    = discount_coupon.objects.aggregate(s=Sum('used_count'))['s'] or 0

    most_used_prem = premium_coupon.objects.order_by('-used_count').first()
    most_used_disc = discount_coupon.objects.order_by('-used_count').first()
    total_coupon_usage = prem_used + disc_used

    context = {
        'admin_user': request.admin_user,
        'total_farmers': total_farmers,
        'total_buyers': total_buyers,
        'total_crops': total_crops,
        'total_tools': total_tools,
        'total_blogs': total_blogs,
        'total_community': total_community,
        'total_orders': total_orders,
        'total_news': total_news,
        'pending_crops': pending_crops,
        'active_users': active_users,
        'total_revenue': total_revenue,
        'premium_buyers': premium_buyers,
        'pending_kyc': pending_kyc,
        'recent_orders': recent_orders,
        'monthly_order_data': json.dumps(monthly_order_data),
        'monthly_labels': json.dumps(monthly_labels),
        'crop_categories': json.dumps(crop_categories),
        'recent_users': recent_users,
        # Coupons
        'prem_total': prem_total,
        'prem_active': prem_active,
        'prem_expired': prem_expired,
        'prem_used': prem_used,
        'disc_total': disc_total,
        'disc_active': disc_active,
        'disc_expired': disc_expired,
        'disc_used': disc_used,
        'most_used_prem': most_used_prem,
        'most_used_disc': most_used_disc,
        'total_coupon_usage': total_coupon_usage,
    }
    return render(request, 'subadmin/dashboard.html', context)



# ─────────────────────────────────────────────────────────────────────────────
# Farmer Management
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def manage_farmers(request):
    qs = User.objects.filter(role='Farmer').select_related('farmer').order_by('-date_joined')

    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    city = request.GET.get('city', '')

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(contact__icontains=q) | Q(email__icontains=q))
    if status == 'active':
        qs = qs.filter(is_active=True)
    elif status == 'inactive':
        qs = qs.filter(is_active=False)
    if city:
        qs = qs.filter(city__icontains=city)

    context = {
        'admin_user': request.admin_user,
        'farmers': qs,
        'q': q,
        'status': status,
        'city': city,
        'total': qs.count(),
    }
    return render(request, 'subadmin/manage_farmers.html', context)


@check_subadmin
def farmer_detail(request, pk):
    user = get_object_or_404(User, pk=pk, role='Farmer')
    farmer_obj = getattr(user, 'farmer', None)
    crops = crop.objects.filter(user=user).order_by('-created_at')
    tools = FarmerTool.objects.filter(user=user).order_by('-created_at')
    blogs_list = bloag.objects.filter(user=user).order_by('-created_at')
    posts = community_message.objects.filter(sender=user).order_by('-created_at')

    context = {
        'admin_user': request.admin_user,
        'farmer_user': user,
        'farmer': farmer_obj,
        'crops': crops,
        'tools': tools,
        'blogs': blogs_list,
        'posts': posts,
    }
    return render(request, 'subadmin/farmer_detail.html', context)


@check_subadmin
def toggle_farmer(request, pk):
    user = get_object_or_404(User, pk=pk, role='Farmer')
    user.is_active = not user.is_active
    user.save()
    action = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'Farmer {user.name} has been {action}.')
    return redirect('subadmin:manage_farmers')


@check_subadmin
def delete_farmer(request, pk):
    user = get_object_or_404(User, pk=pk, role='Farmer')
    name = user.name
    user.delete()
    messages.success(request, f'Farmer {name} has been permanently deleted.')
    return redirect('subadmin:manage_farmers')


@check_subadmin
def reset_farmer_password(request, pk):
    user = get_object_or_404(User, pk=pk, role='Farmer')
    if request.method == 'POST':
        new_pw = request.POST.get('new_password', '').strip()
        if len(new_pw) < 4:
            messages.error(request, 'Password must be at least 4 characters.')
            return redirect('subadmin:farmer_detail', pk=pk)
        user.password = make_password(new_pw)
        user.save()
        messages.success(request, f'Password for {user.name} has been reset.')
    return redirect('subadmin:farmer_detail', pk=pk)


@check_subadmin
def grant_doc_permission(request, pk):
    farmer_obj = get_object_or_404(Farmer, user_id=pk)
    farmer_obj.doc_edit_permission = not farmer_obj.doc_edit_permission
    farmer_obj.save()
    state = 'granted' if farmer_obj.doc_edit_permission else 'revoked'
    messages.success(request, f'Document edit permission {state} for {farmer_obj.user.name}.')
    return redirect('subadmin:farmer_detail', pk=pk)


# ─────────────────────────────────────────────────────────────────────────────
# Buyer Management
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def manage_buyers(request):
    qs = Buyer.objects.select_related('user').order_by('-created_at')

    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    verified = request.GET.get('verified', '')

    if q:
        qs = qs.filter(
            Q(user__name__icontains=q) |
            Q(user__contact__icontains=q) |
            Q(user__email__icontains=q) |
            Q(gst_no__icontains=q)
        )
    if status == 'active':
        qs = qs.filter(user__is_active=True)
    elif status == 'inactive':
        qs = qs.filter(user__is_active=False)
    if verified == 'yes':
        qs = qs.filter(is_verified=True)
    elif verified == 'no':
        qs = qs.filter(is_verified=False)

    context = {
        'admin_user': request.admin_user,
        'buyers': qs,
        'q': q,
        'status': status,
        'verified': verified,
        'total': qs.count(),
    }
    return render(request, 'subadmin/manage_buyers.html', context)


@check_subadmin
def buyer_detail(request, pk):
    buyer_obj = get_object_or_404(Buyer, pk=pk)
    orders = Order.objects.filter(user=buyer_obj.user).order_by('-created_at')
    premiums = premium_buyer.objects.filter(user=buyer_obj).order_by('-purchase_date')

    context = {
        'admin_user': request.admin_user,
        'buyer': buyer_obj,
        'orders': orders,
        'premiums': premiums,
    }
    return render(request, 'subadmin/buyer_detail.html', context)


@check_subadmin
def toggle_buyer(request, pk):
    buyer_obj = get_object_or_404(Buyer, pk=pk)
    user = buyer_obj.user
    user.is_active = not user.is_active
    user.save()
    action = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'Buyer {user.name} has been {action}.')
    return redirect('subadmin:manage_buyers')


@check_subadmin
def delete_buyer(request, pk):
    buyer_obj = get_object_or_404(Buyer, pk=pk)
    name = buyer_obj.user.name
    buyer_obj.user.delete()
    messages.success(request, f'Buyer {name} has been permanently deleted.')
    return redirect('subadmin:manage_buyers')


@check_subadmin
def verify_buyer(request, pk):
    buyer_obj = get_object_or_404(Buyer, pk=pk)
    buyer_obj.is_verified = not buyer_obj.is_verified
    buyer_obj.save()
    state = 'verified' if buyer_obj.is_verified else 'unverified'
    messages.success(request, f'Buyer {buyer_obj.user.name} has been {state}.')
    return redirect('subadmin:buyer_detail', pk=pk)


# ─────────────────────────────────────────────────────────────────────────────
# Crop Management
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def manage_crops(request):
    qs = crop.objects.select_related('user').order_by('-created_at')

    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')

    if q:
        qs = qs.filter(Q(cropname__icontains=q) | Q(user__name__icontains=q))
    if category:
        qs = qs.filter(category=category)
    if status == 'approved':
        qs = qs.filter(is_approved=True)
    elif status == 'pending':
        qs = qs.filter(is_approved=False)

    context = {
        'admin_user': request.admin_user,
        'crops': qs,
        'q': q,
        'category': category,
        'status': status,
        'total': qs.count(),
        'category_choices': crop.CATEGORY_CHOICES,
    }
    return render(request, 'subadmin/manage_crops.html', context)


@check_subadmin
def crop_approve(request, pk):
    c = get_object_or_404(crop, pk=pk)
    c.is_approved = True
    c.save()
    messages.success(request, f'Crop "{c.cropname}" approved.')
    return redirect(request.META.get('HTTP_REFERER', 'subadmin:manage_crops'))


@check_subadmin
def crop_reject(request, pk):
    c = get_object_or_404(crop, pk=pk)
    c.is_approved = False
    c.save()
    messages.success(request, f'Crop "{c.cropname}" rejected/unpublished.')
    return redirect(request.META.get('HTTP_REFERER', 'subadmin:manage_crops'))


@check_subadmin
def crop_delete(request, pk):
    c = get_object_or_404(crop, pk=pk)
    name = c.cropname
    c.delete()
    messages.success(request, f'Crop "{name}" deleted.')
    return redirect('subadmin:manage_crops')


# ─────────────────────────────────────────────────────────────────────────────
# Tool Management
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def manage_tools(request):
    qs = FarmerTool.objects.select_related('user').order_by('-created_at')

    q = request.GET.get('q', '')
    category = request.GET.get('category', '')

    if q:
        qs = qs.filter(Q(tool_name__icontains=q) | Q(user__name__icontains=q))
    if category:
        qs = qs.filter(category=category)

    context = {
        'admin_user': request.admin_user,
        'tools': qs,
        'q': q,
        'category': category,
        'total': qs.count(),
        'category_choices': FarmerTool.CATEGORY_CHOICES,
    }
    return render(request, 'subadmin/manage_tools.html', context)


@check_subadmin
def tool_delete(request, pk):
    t = get_object_or_404(FarmerTool, pk=pk)
    name = t.tool_name
    t.delete()
    messages.success(request, f'Tool "{name}" deleted.')
    return redirect('subadmin:manage_tools')


# ─────────────────────────────────────────────────────────────────────────────
# Blog Management
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def manage_blogs(request):
    qs = bloag.objects.select_related('user').order_by('-created_at')

    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(user__name__icontains=q))

    context = {
        'admin_user': request.admin_user,
        'blogs': qs,
        'q': q,
        'total': qs.count(),
    }
    return render(request, 'subadmin/manage_blogs.html', context)


@check_subadmin
def blog_delete(request, pk):
    b = get_object_or_404(bloag, pk=pk)
    title = b.title or 'Untitled'
    b.delete()
    messages.success(request, f'Blog "{title}" deleted.')
    return redirect('subadmin:manage_blogs')


# ─────────────────────────────────────────────────────────────────────────────
# Community Management
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def manage_community(request):
    qs = community_message.objects.select_related('sender').order_by('-created_at')

    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(Q(message__icontains=q) | Q(sender__name__icontains=q))

    context = {
        'admin_user': request.admin_user,
        'posts': qs,
        'q': q,
        'total': qs.count(),
    }
    return render(request, 'subadmin/manage_community.html', context)


@check_subadmin
def community_delete(request, pk):
    post = get_object_or_404(community_message, pk=pk)
    post.delete()
    messages.success(request, 'Community post deleted.')
    return redirect('subadmin:manage_community')


# ─────────────────────────────────────────────────────────────────────────────
# News Management
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def manage_news(request):
    qs = news.objects.order_by('-created_at')

    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    state = request.GET.get('state', '')

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category:
        qs = qs.filter(category=category)
    if state:
        qs = qs.filter(state=state)

    context = {
        'admin_user': request.admin_user,
        'all_news': qs,
        'q': q,
        'category': category,
        'state': state,
        'total': qs.count(),
        'category_choices': news.category_choices,
        'state_choices': news.STATE_CHOICES,
    }
    return render(request, 'subadmin/manage_news.html', context)


@check_subadmin
def news_add(request):
    if request.method == 'POST':
        try:
            n = news(
                title=request.POST.get('title', '').strip(),
                description=request.POST.get('description', '').strip(),
                category=request.POST.get('category', ''),
                state=request.POST.get('state', ''),
                source_link=request.POST.get('source_link', '') or None,
                is_breaking=request.POST.get('is_breaking') == 'on',
                breaking_hours=int(request.POST.get('breaking_hours', 24) or 24),
            )
            if request.FILES.get('image'):
                n.image = request.FILES['image']
            n.save()
            messages.success(request, f'News "{n.title}" published.')
            return redirect('subadmin:manage_news')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    context = {
        'admin_user': request.admin_user,
        'category_choices': news.category_choices,
        'state_choices': news.STATE_CHOICES,
        'action': 'Add',
    }
    return render(request, 'subadmin/news_form.html', context)


@check_subadmin
def news_edit(request, pk):
    n = get_object_or_404(news, pk=pk)
    if request.method == 'POST':
        try:
            n.title = request.POST.get('title', n.title).strip()
            n.description = request.POST.get('description', n.description).strip()
            n.category = request.POST.get('category', n.category)
            n.state = request.POST.get('state', n.state)
            n.source_link = request.POST.get('source_link', '') or None
            n.is_breaking = request.POST.get('is_breaking') == 'on'
            n.breaking_hours = int(request.POST.get('breaking_hours', n.breaking_hours) or 24)
            if request.FILES.get('image'):
                n.image = request.FILES['image']
            n.save()
            messages.success(request, f'News "{n.title}" updated.')
            return redirect('subadmin:manage_news')
        except Exception as e:
            messages.error(request, f'Error: {e}')

    context = {
        'admin_user': request.admin_user,
        'news_obj': n,
        'category_choices': news.category_choices,
        'state_choices': news.STATE_CHOICES,
        'action': 'Edit',
    }
    return render(request, 'subadmin/news_form.html', context)


@check_subadmin
def news_delete(request, pk):
    n = get_object_or_404(news, pk=pk)
    title = n.title
    n.delete()
    messages.success(request, f'News "{title}" deleted.')
    return redirect('subadmin:manage_news')


@check_subadmin
def news_toggle_breaking(request, pk):
    n = get_object_or_404(news, pk=pk)
    n.is_breaking = not n.is_breaking
    n.save()
    state = 'marked as Breaking News' if n.is_breaking else 'removed from Breaking News'
    messages.success(request, f'"{n.title}" {state}.')
    return redirect('subadmin:manage_news')


# ─────────────────────────────────────────────────────────────────────────────
# Order Management
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def manage_orders(request):
    qs = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')

    q = request.GET.get('q', '')
    status = request.GET.get('status', '')

    if q:
        qs = qs.filter(Q(order_id__icontains=q) | Q(user__name__icontains=q))
    if status:
        qs = qs.filter(status=status)

    context = {
        'admin_user': request.admin_user,
        'orders': qs,
        'q': q,
        'status': status,
        'total': qs.count(),
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'subadmin/manage_orders.html', context)


@check_subadmin
def order_detail(request, pk):
    o = get_object_or_404(Order, pk=pk)
    items = o.items.select_related('crop').all()
    context = {
        'admin_user': request.admin_user,
        'order': o,
        'items': items,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'subadmin/order_detail.html', context)


@check_subadmin
def order_update_status(request, pk):
    o = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status', '')
        valid = [s[0] for s in Order.STATUS_CHOICES]
        if new_status in valid:
            o.status = new_status
            o.save()
            messages.success(request, f'Order {o.order_id} status updated to {new_status}.')
        else:
            messages.error(request, 'Invalid status.')
    return redirect('subadmin:order_detail', pk=pk)


# ─────────────────────────────────────────────────────────────────────────────
# KYC Approval
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def kyc_approval(request):
    # Farmers who uploaded at least one document
    farmers_with_docs = Farmer.objects.select_related('user').filter(
        Q(adharcard__isnull=False) | Q(pancard__isnull=False)
    ).exclude(adharcard='').order_by('-created_at')

    q = request.GET.get('q', '')
    if q:
        farmers_with_docs = farmers_with_docs.filter(
            Q(user__name__icontains=q) | Q(adharno__icontains=q)
        )

    context = {
        'admin_user': request.admin_user,
        'farmers': farmers_with_docs,
        'q': q,
        'total': farmers_with_docs.count(),
    }
    return render(request, 'subadmin/kyc_approval.html', context)


@check_subadmin
def kyc_grant_doc(request, pk):
    farmer_obj = get_object_or_404(Farmer, user_id=pk)
    farmer_obj.doc_edit_permission = True
    farmer_obj.save()
    messages.success(request, f'Document edit permission granted to {farmer_obj.user.name}.')
    return redirect('subadmin:kyc_approval')


# ─────────────────────────────────────────────────────────────────────────────
# Product / Crop Approval
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def product_approval(request):
    pending = crop.objects.filter(is_approved=False).select_related('user').order_by('-created_at')

    q = request.GET.get('q', '')
    if q:
        pending = pending.filter(Q(cropname__icontains=q) | Q(user__name__icontains=q))

    context = {
        'admin_user': request.admin_user,
        'pending_crops': pending,
        'q': q,
        'total': pending.count(),
    }
    return render(request, 'subadmin/product_approval.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# Premium Management
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def premium_settings(request):
    try:
        plan = premium_plans.objects.get()
    except premium_plans.DoesNotExist:
        plan = premium_plans.objects.create(standard_price=99, premium_price=199, year_dis=20)
    except premium_plans.MultipleObjectsReturned:
        plan = premium_plans.objects.first()

    if request.method == 'POST':
        try:
            sp = request.POST.get('standard_price', '')
            pp = request.POST.get('premium_price', '')
            yd = request.POST.get('year_dis', '')
            
            if sp == '' or pp == '' or yd == '':
                messages.error(request, 'All fields are required.')
            else:
                sp = int(sp)
                pp = int(pp)
                yd = int(yd)
                
                if sp < 0 or pp < 0:
                    messages.error(request, 'Prices cannot be negative.')
                elif yd < 0 or yd > 100:
                    messages.error(request, 'Yearly discount must be between 0 and 100.')
                else:
                    plan.standard_price = sp
                    plan.premium_price = pp
                    plan.year_dis = yd
                    plan.save()
                    messages.success(request, 'Premium plan prices updated successfully.')
        except ValueError:
            messages.error(request, 'Invalid input. Please enter valid numbers.')
            
        return redirect('subadmin:premium_settings')

    context = {
        'admin_user': request.admin_user,
        'plan': plan,
        'nav_premium_settings': 'active'
    }
    return render(request, 'subadmin/premium_settings.html', context)


@check_subadmin
def manage_premium(request):
    buyer_prems = list(premium_buyer.objects.select_related('user', 'user__user').order_by('-purchase_date'))
    for b in buyer_prems:
        b.user_role = 'Buyer'
        
    farmer_prems = list(farmer_premium_buyer.objects.select_related('user', 'user__user').order_by('-purchase_date'))
    for f in farmer_prems:
        f.user_role = 'Farmer'

    all_prems = buyer_prems + farmer_prems
    all_prems.sort(key=lambda x: x.purchase_date, reverse=True)

    q = request.GET.get('q', '').strip()
    plan = request.GET.get('plan', '')
    user_type = request.GET.get('user_type', '')

    if q:
        all_prems = [p for p in all_prems if q.lower() in p.user.user.name.lower()]
    if plan:
        all_prems = [p for p in all_prems if p.premium_type == plan]
    if user_type:
        all_prems = [p for p in all_prems if p.user_role == user_type]

    context = {
        'admin_user': request.admin_user,
        'premiums': all_prems,
        'q': q,
        'plan': plan,
        'user_type': user_type,
        'total': len(all_prems),
    }
    return render(request, 'subadmin/manage_premium.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# Reports & CSV Exports
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def reports(request):
    total_revenue = OrderItem.objects.aggregate(s=Sum('subtotal'))['s'] or 0
    context = {
        'admin_user': request.admin_user,
        'total_revenue': int(total_revenue),
        'total_farmers': Farmer.objects.count(),
        'total_buyers': Buyer.objects.count(),
        'total_orders': Order.objects.count(),
        'total_crops': crop.objects.count(),
        'total_tools': FarmerTool.objects.count(),
    }
    return render(request, 'subadmin/reports.html', context)


@check_subadmin
def export_farmers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="farmers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Contact', 'Email', 'City', 'Farm Name', 'Acres', 'Status', 'Joined'])
    for f in Farmer.objects.select_related('user').all():
        writer.writerow([
            f.user.name, f.user.contact, f.user.email or '',
            f.user.city or '', f.farm_name or '', f.acres or '',
            'Active' if f.user.is_active else 'Inactive',
            f.user.date_joined.strftime('%Y-%m-%d'),
        ])
    return response


@check_subadmin
def export_buyers_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="buyers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Contact', 'Email', 'State', 'GST No', 'Verified', 'Premium', 'Joined'])
    for b in Buyer.objects.select_related('user').all():
        writer.writerow([
            b.user.name, b.user.contact, b.user.email or '',
            b.state, b.gst_no or '',
            'Yes' if b.is_verified else 'No',
            'Yes' if b.is_premiume else 'No',
            b.created_at.strftime('%Y-%m-%d'),
        ])
    return response


@check_subadmin
def export_orders_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Buyer', 'Total Amount', 'Status', 'Payment', 'Date'])
    for o in Order.objects.select_related('user').all():
        writer.writerow([
            o.order_id, o.user.name, str(o.total_amount),
            o.status, o.payment_status,
            o.created_at.strftime('%Y-%m-%d'),
        ])
    return response


# ─────────────────────────────────────────────────────────────────────────────
# Profile & Settings (enhanced placeholders)
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def profile(request):
    context = {'admin_user': request.admin_user}
    return render(request, 'subadmin/profile.html', context)


@check_subadmin
def support_tickets(request):
    context = {'admin_user': request.admin_user}
    return render(request, 'subadmin/support_tickets.html', context)


@check_subadmin
def system_settings(request):
    context = {'admin_user': request.admin_user}
    return render(request, 'subadmin/system_settings.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# Coupon helpers
# ─────────────────────────────────────────────────────────────────────────────

def _coupon_is_expired(c):
    from django.utils import timezone
    return c.expiry_date is not None and timezone.now() > c.expiry_date


# ─────────────────────────────────────────────────────────────────────────────
# Premium Coupon Management
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def manage_premium_coupons(request):
    qs = premium_coupon.objects.order_by('-created_at')

    q       = request.GET.get('q', '')
    status  = request.GET.get('status', '')
    expired = request.GET.get('expired', '')

    if q:
        qs = qs.filter(Q(code__icontains=q) | Q(label__icontains=q))
    if status == 'active':
        qs = qs.filter(is_active=True)
    elif status == 'inactive':
        qs = qs.filter(is_active=False)

    now = timezone.now()
    if expired == 'yes':
        qs = qs.filter(expiry_date__lt=now)
    elif expired == 'no':
        qs = qs.filter(Q(expiry_date__isnull=True) | Q(expiry_date__gte=now))

    # Stats
    total_all     = premium_coupon.objects.count()
    total_active  = premium_coupon.objects.filter(is_active=True).count()
    total_expired = premium_coupon.objects.filter(expiry_date__lt=now).count()
    total_used    = premium_coupon.objects.aggregate(s=Sum('used_count'))['s'] or 0
    most_used     = premium_coupon.objects.order_by('-used_count').first()

    context = {
        'admin_user': request.admin_user,
        'coupons': qs,
        'q': q, 'status': status, 'expired': expired,
        'total': qs.count(),
        'total_all': total_all,
        'total_active': total_active,
        'total_expired': total_expired,
        'total_used': total_used,
        'most_used': most_used,
        'coupon_type': 'premium',
    }
    return render(request, 'subadmin/manage_coupons.html', context)


@check_subadmin
def premium_coupon_add(request):
    if request.method == 'POST':
        try:
            import decimal
            expiry_raw = request.POST.get('expiry_date', '').strip()
            from django.utils.dateparse import parse_datetime
            expiry = parse_datetime(expiry_raw) if expiry_raw else None

            premium_coupon.objects.create(
                code           = request.POST.get('code', '').strip().upper(),
                label          = request.POST.get('label', '').strip(),
                discount_type  = request.POST.get('discount_type', 'percent'),
                discount_value = decimal.Decimal(request.POST.get('discount_value', 0)),
                minimum_amount = decimal.Decimal(request.POST.get('minimum_amount', 0)),
                usage_limit    = int(request.POST.get('usage_limit', 100)),
                expiry_date    = expiry,
                is_active      = request.POST.get('is_active') == 'on',
            )
            messages.success(request, 'Premium coupon created successfully.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('subadmin:manage_premium_coupons')
    context = {'admin_user': request.admin_user, 'coupon_type': 'premium', 'action': 'Add'}
    return render(request, 'subadmin/coupon_form.html', context)


@check_subadmin
def premium_coupon_edit(request, pk):
    c = get_object_or_404(premium_coupon, pk=pk)
    if request.method == 'POST':
        try:
            import decimal
            from django.utils.dateparse import parse_datetime
            expiry_raw = request.POST.get('expiry_date', '').strip()
            expiry = parse_datetime(expiry_raw) if expiry_raw else None

            c.code           = request.POST.get('code', c.code).strip().upper()
            c.label          = request.POST.get('label', c.label).strip()
            c.discount_type  = request.POST.get('discount_type', c.discount_type)
            c.discount_value = decimal.Decimal(request.POST.get('discount_value', c.discount_value))
            c.minimum_amount = decimal.Decimal(request.POST.get('minimum_amount', c.minimum_amount))
            c.usage_limit    = int(request.POST.get('usage_limit', c.usage_limit))
            c.expiry_date    = expiry
            c.is_active      = request.POST.get('is_active') == 'on'
            c.save()
            messages.success(request, f'Coupon "{c.code}" updated.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('subadmin:manage_premium_coupons')
    context = {
        'admin_user': request.admin_user,
        'coupon_obj': c,
        'coupon_type': 'premium',
        'action': 'Edit',
    }
    return render(request, 'subadmin/coupon_form.html', context)


@check_subadmin
def premium_coupon_delete(request, pk):
    c = get_object_or_404(premium_coupon, pk=pk)
    code = c.code
    c.delete()
    messages.success(request, f'Coupon "{code}" deleted.')
    return redirect('subadmin:manage_premium_coupons')


@check_subadmin
def premium_coupon_toggle(request, pk):
    c = get_object_or_404(premium_coupon, pk=pk)
    c.is_active = not c.is_active
    c.save()
    state = 'activated' if c.is_active else 'deactivated'
    messages.success(request, f'Coupon "{c.code}" {state}.')
    return redirect('subadmin:manage_premium_coupons')


@check_subadmin
def premium_coupon_duplicate(request, pk):
    c = get_object_or_404(premium_coupon, pk=pk)
    import uuid
    new_code = f'{c.code}-{uuid.uuid4().hex[:4].upper()}'
    try:
        premium_coupon.objects.create(
            code=new_code, label=c.label,
            discount_type=c.discount_type, discount_value=c.discount_value,
            minimum_amount=c.minimum_amount, usage_limit=c.usage_limit,
            expiry_date=c.expiry_date, is_active=False,
        )
        messages.success(request, f'Coupon duplicated as "{new_code}" (inactive by default).')
    except Exception as e:
        messages.error(request, f'Duplicate failed: {e}')
    return redirect('subadmin:manage_premium_coupons')


# ─────────────────────────────────────────────────────────────────────────────
# Discount Coupon Management
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def manage_discount_coupons(request):
    qs = discount_coupon.objects.order_by('-created_at')

    q      = request.GET.get('q', '')
    status = request.GET.get('status', '')
    now    = timezone.now()

    if q:
        qs = qs.filter(Q(code__icontains=q) | Q(label__icontains=q))
    if status == 'active':
        qs = qs.filter(is_active=True)
    elif status == 'inactive':
        qs = qs.filter(is_active=False)

    total_all     = discount_coupon.objects.count()
    total_active  = discount_coupon.objects.filter(is_active=True).count()
    total_expired = discount_coupon.objects.filter(expiry_date__lt=now).count()
    total_used    = discount_coupon.objects.aggregate(s=Sum('used_count'))['s'] or 0
    most_used     = discount_coupon.objects.order_by('-used_count').first()

    context = {
        'admin_user': request.admin_user,
        'coupons': qs,
        'q': q, 'status': status,
        'total': qs.count(),
        'total_all': total_all,
        'total_active': total_active,
        'total_expired': total_expired,
        'total_used': total_used,
        'most_used': most_used,
        'coupon_type': 'discount',
    }
    return render(request, 'subadmin/manage_coupons.html', context)


@check_subadmin
def discount_coupon_add(request):
    if request.method == 'POST':
        try:
            import decimal
            from django.utils.dateparse import parse_datetime
            expiry_raw = request.POST.get('expiry_date', '').strip()
            expiry = parse_datetime(expiry_raw) if expiry_raw else None
            discount_coupon.objects.create(
                code           = request.POST.get('code', '').strip().upper(),
                label          = request.POST.get('label', '').strip(),
                discount_type  = request.POST.get('discount_type', 'percent'),
                discount_value = decimal.Decimal(request.POST.get('discount_value', 0)),
                minimum_amount = decimal.Decimal(request.POST.get('minimum_amount', 0)),
                usage_limit    = int(request.POST.get('usage_limit', 100)),
                expiry_date    = expiry,
                is_active      = request.POST.get('is_active') == 'on',
            )
            messages.success(request, 'Discount coupon created.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('subadmin:manage_discount_coupons')
    context = {'admin_user': request.admin_user, 'coupon_type': 'discount', 'action': 'Add'}
    return render(request, 'subadmin/coupon_form.html', context)


@check_subadmin
def discount_coupon_edit(request, pk):
    c = get_object_or_404(discount_coupon, pk=pk)
    if request.method == 'POST':
        try:
            import decimal
            from django.utils.dateparse import parse_datetime
            expiry_raw = request.POST.get('expiry_date', '').strip()
            expiry = parse_datetime(expiry_raw) if expiry_raw else None
            c.code           = request.POST.get('code', c.code).strip().upper()
            c.label          = request.POST.get('label', c.label).strip()
            c.discount_type  = request.POST.get('discount_type', c.discount_type)
            c.discount_value = decimal.Decimal(request.POST.get('discount_value', c.discount_value))
            c.minimum_amount = decimal.Decimal(request.POST.get('minimum_amount', c.minimum_amount))
            c.usage_limit    = int(request.POST.get('usage_limit', c.usage_limit))
            c.expiry_date    = expiry
            c.is_active      = request.POST.get('is_active') == 'on'
            c.save()
            messages.success(request, f'Coupon "{c.code}" updated.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect('subadmin:manage_discount_coupons')
    context = {'admin_user': request.admin_user, 'coupon_obj': c, 'coupon_type': 'discount', 'action': 'Edit'}
    return render(request, 'subadmin/coupon_form.html', context)


@check_subadmin
def discount_coupon_delete(request, pk):
    c = get_object_or_404(discount_coupon, pk=pk)
    code = c.code
    c.delete()
    messages.success(request, f'Coupon "{code}" deleted.')
    return redirect('subadmin:manage_discount_coupons')


@check_subadmin
def discount_coupon_toggle(request, pk):
    c = get_object_or_404(discount_coupon, pk=pk)
    c.is_active = not c.is_active
    c.save()
    state = 'activated' if c.is_active else 'deactivated'
    messages.success(request, f'Coupon "{c.code}" {state}.')
    return redirect('subadmin:manage_discount_coupons')


# ─────────────────────────────────────────────────────────────────────────────
# Transactions / Payment History
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def transactions(request):
    qs = premium_history.objects.select_related('user', 'user__user').order_by('-start_date')

    q    = request.GET.get('q', '')
    plan = request.GET.get('plan', '')
    date = request.GET.get('date', '')

    if q:
        qs = qs.filter(Q(user__user__name__icontains=q) | Q(user__user__contact__icontains=q))
    if plan:
        qs = qs.filter(plan=plan)
    if date:
        qs = qs.filter(start_date__date=date)

    total_revenue = qs.aggregate(s=Sum('price'))['s'] or 0

    context = {
        'admin_user': request.admin_user,
        'transactions': qs,
        'q': q, 'plan': plan, 'date': date,
        'total': qs.count(),
        'total_revenue': int(total_revenue),
    }
    return render(request, 'subadmin/transactions.html', context)


@check_subadmin
def export_premium_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="premium_users.csv"'
    writer = csv.writer(response)
    writer.writerow(['Buyer', 'Contact', 'Plan', 'Billing', 'Purchase Date'])
    for p in premium_buyer.objects.select_related('user', 'user__user').all():
        writer.writerow([
            p.user.user.name, p.user.user.contact,
            p.premium_type, p.premium_time,
            p.purchase_date.strftime('%Y-%m-%d'),
        ])
    return response


@check_subadmin
def export_transactions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    writer = csv.writer(response)
    writer.writerow(['Buyer', 'Contact', 'Plan', 'Billing', 'Price', 'Coupon', 'Date'])
    for t in premium_history.objects.select_related('user', 'user__user').all():
        writer.writerow([
            t.user.user.name, t.user.user.contact,
            t.plan, t.billing_cycle, t.price,
            t.coupon_code or '—',
            t.start_date.strftime('%Y-%m-%d'),
        ])
    return response


# ─────────────────────────────────────────────────────────────────────────────
# Premium Subscription Actions (manual admin control)
# ─────────────────────────────────────────────────────────────────────────────

@check_subadmin
def premium_manual_upgrade(request, pk):
    """Admin force-upgrades/downgrades a buyer or farmer plan."""
    user_role = request.POST.get('user_role', '')
    if user_role == 'Farmer':
        p = get_object_or_404(farmer_premium_buyer, pk=pk)
    elif user_role == 'Buyer':
        p = get_object_or_404(premium_buyer, pk=pk)
    else:
        p = premium_buyer.objects.filter(pk=pk).first() or get_object_or_404(farmer_premium_buyer, pk=pk)

    if request.method == 'POST':
        new_plan  = request.POST.get('plan', p.premium_type)
        new_cycle = request.POST.get('cycle', p.premium_time)
        p.premium_type  = new_plan
        p.premium_time  = new_cycle
        p.purchase_date = timezone.now()
        p.save()

        if hasattr(p.user, 'is_premiume'):
            p.user.is_premiume = (new_plan != 'Free')
            p.user.save()
        else:
            from farmer.views import update_farmer_limit
            update_farmer_limit(p.user, new_plan)

        messages.success(request, f'Plan for {p.user.user.name} updated to {new_plan} ({new_cycle}).')
    return redirect('subadmin:manage_premium')


@check_subadmin
def premium_cancel(request, pk):
    """Admin cancels a subscription (reverts to Free)."""
    user_role = request.GET.get('user_role', '')
    if user_role == 'Farmer':
        p = get_object_or_404(farmer_premium_buyer, pk=pk)
    elif user_role == 'Buyer':
        p = get_object_or_404(premium_buyer, pk=pk)
    else:
        p = premium_buyer.objects.filter(pk=pk).first() or get_object_or_404(farmer_premium_buyer, pk=pk)

    user_name = p.user.user.name
    p.premium_type = 'Free'
    p.premium_time = 'Monthly'
    p.save()

    if hasattr(p.user, 'is_premiume'):
        p.user.is_premiume = False
        p.user.save()
    else:
        from farmer.views import update_farmer_limit
        update_farmer_limit(p.user, 'Free')

    messages.success(request, f'Subscription for {user_name} cancelled (reverted to Free).')
    return redirect('subadmin:manage_premium')

