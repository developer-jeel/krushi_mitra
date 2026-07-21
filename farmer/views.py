import json
import math
import random
from pathlib import Path

import joblib
import pandas as pd
import requests
import sseclient

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.core.cache import cache
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression

from buyer.models import *
from .models import *



BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

PRICE_MODEL = DATA_DIR / "price_model.pkl"
RAIN_MODEL = DATA_DIR / "rain_model.pkl"


# ---------------- PRICE MODEL ----------------

if not PRICE_MODEL.exists():

    df = pd.read_csv(DATA_DIR / "tool_prices_1000000_dataset.csv")

    X = df[["category", "years", "condition"]]
    y = df["rate"].apply(math.log)

    price_model = LinearRegression()
    price_model.fit(X, y)

    joblib.dump(price_model, PRICE_MODEL)

else:
    price_model = joblib.load(PRICE_MODEL)


# ---------------- RAIN MODEL ----------------

if not RAIN_MODEL.exists():

    df = pd.read_csv(DATA_DIR / "weather_prediction.csv")

    X = df[["temperature", "humidity", "wind_speed", "clouds"]]
    y = df["rain"]

    rain_model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    rain_model.fit(X, y)

    joblib.dump(rain_model, RAIN_MODEL)

else:
    rain_model = joblib.load(RAIN_MODEL)

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_pw = request.POST.get('confirmPw')
        aadhar = request.POST.get('aadhar')
        
        # Validation
        if password != confirm_pw:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
            
        if User.objects.filter(contact=contact).exists():
            messages.error(request, 'Contact number already registered')
            return redirect('register')
            
        try:
            # Create user
            user = User.objects.create(
                username=contact,  # Using contact as username
                name=name,
                contact=contact,
                role=role,
                password=make_password(password)
            )
            
            # Create specific profile
            if role == 'Farmer':
                Farmer.objects.create(user=user, adharno=aadhar)
            elif role == 'Buyer':
                gst = request.POST.get('gst')
                Buyer.objects.create(user=user, gst_no=gst)
                
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return redirect('register')
            
    return render(request, "farmer/register.html")

def login(request):
    if request.method == 'POST':
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        
        user = User.objects.filter(contact=contact).first()

        if user is not None and check_password(password, user.password):
            if user.scheduled_deletion_date:
                if user.scheduled_deletion_date <= timezone.now():
                    user.delete()
                    messages.error(request, 'Your account has been permanently deleted.')
                    return redirect('login')
                else:
                    user.scheduled_deletion_date = None
                    user.save()
                    messages.success(request, 'Your account deletion request has been cancelled.')


            # Buyer verification check
            # if user.role == 'Buyer':
            #     if not hasattr(user, 'buyer') or not user.buyer.is_verified:
            #         messages.error(request, 'Sorry you are not verified yet')
            #         return redirect('login')

            # SESSION SET
            request.session['contact'] = user.contact

            #  Redirect based on role
            if user.role == 'Farmer':
                user.is_active = True
                user.save()
                return redirect('farmer_home')
            elif user.role == 'Buyer':
                user.is_active = True
                user.save()
                return redirect('buyer_home')
            else:
                return redirect('home')

        else:
            messages.error(request, 'Invalid Contact number or password')
            return redirect('login')
            
    return render(request, "farmer/login.html")

def check_login(allowed_roles):
    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            if "contact" in request.session:
                try:
                    user = User.objects.get(contact=request.session['contact'])
                    request.uid = user

                    #  Role check
                    if user.role not in allowed_roles:
                        messages.error(request, "Access Denied")
                        return redirect('login')


                    #  Buyer verification
                    # if user.role == 'Buyer':
                    #     if not hasattr(user, 'buyer') or not user.buyer.is_verified:
                    #         messages.error(request, "Not verified")
                    #         return redirect('login')

                    return view_function(request, *args, **kwargs)

                except User.DoesNotExist:
                    return redirect('login')

            return redirect('login')
        return wrapper
    return decorator


def crop_price(city):
    api_key = "579b464db66ec23bdd0000012bddf55026c442586adb6f1fa0b82807"
    resource_id = "9ef84268-d588-465a-a308-a864a43d0070"
    
    url = f"https://api.data.gov.in/resource/{resource_id}?api-key={api_key}&format=json&filters[state]=Gujarat&filters[district]={city}&limit=1000"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    prices = []
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        data = response.json()
        records = data.get("records", [])
        
        # Look for our target crops in the records
        for record in records:
                prices.append({
                    "crop": record.get("commodity"),
                    "price": record.get("modal_price") // 100 * 20,  # Convert to price per 20kg
                    "price_range": f"{record.get('min_price')} - {record.get('max_price')}"
                })  # Stop searching for this crop once we find the first price
                    
    except Exception as e:
        print(f"Error fetching data: {e}")
        
    return prices

@check_login(['Farmer'])
def farmer_home(request):
    uid = request.uid
    city = uid.city
    crop_prices = crop_price(city)
    random.shuffle(crop_prices)
    crop_prices = crop_prices[:6]
    all_news = news.objects.all().order_by('-created_at')[:4]
    bolgs = bloag.objects.all().order_by('-created_at')[:3]
    schemes = gov_info.objects.all().order_by('-created_at')[:4]
    context = {"crop_prices": crop_prices,'uid' : uid, 'all_news': all_news, 'bolgs': bolgs, 'schemes': schemes,'city' : city}

    return render(request, "farmer/home.html",context)

@check_login(['Farmer'])
def farmer_crops(request):
    uid = request.uid
    all_crops = crop.objects.filter(user=uid).order_by('-created_at')
    context = {"uid" : uid , "all_crops" : all_crops}
    if request.method == "POST":
        cropname = request.POST.get("cropname")
        category = request.POST.get("category")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image = request.FILES.get('image')

        crop.objects.create(
            user = uid,
            cropname = cropname,
            category = category,
            quantity = quantity,
            price = price,
            description = description,
            image = image,
            is_approved = False
        )
    
        return redirect('farmer_crops')
    return render(request, "farmer/crops.html",context)

@check_login(['Farmer'])
def farmer_tools(request):
    uid = request.uid
    qs = FarmerTool.objects.filter(availability_status='available').exclude(user=uid).order_by('-created_at')
    
    # Attach predicted price to each tool
    available_tools = []
    for t in qs:
        predicted = _tool_predicted_price(t.category, t.condition, t.years_used, t.original_price)
        available_tools.append({'tool': t, 'predicted_price': predicted})
        
    context = {'uid': uid, 'available_tools': available_tools}
    return render(request, "farmer/tools.html", context)

@check_login(['Farmer'])
def farmer_blogs(request):
    uid = request.uid
    all_blogs = bloag.objects.exclude(user=uid).order_by('-created_at')    
    print(all_blogs)
    context = { 'uid' : uid , 'all_blogs' : all_blogs}
    return render(request, "farmer/view_blogs.html",context)

@check_login(['Farmer'])
def write_blog(request):
    uid = request.uid
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        image = request.FILES.get('image')
        video = request.FILES.get('video')
        
        create_bloag = bloag.objects.create(
            user = uid,
            title = title,
            content = content
        )
        if image:
            create_bloag.image = image
        if video:
            create_bloag.video = video
        create_bloag.save()

        return render(request, "farmer/write_blog.html")
    return render(request, "farmer/write_blog.html")

@check_login(['Farmer'])
def my_posts(request):
    uid = request.uid
    blogs = bloag.objects.filter(user = uid).order_by('-created_at')
    print(blogs)
    context = { 'uid' : uid , 'my_blogs' :blogs}
    return render(request,"farmer/my_post.html",context)
    
@check_login(['Farmer'])
def delete_blog(request):
    return render(request,"farmer/my_post.html")


@check_login(['Farmer'])
def farmer_profile(request):
    uid = request.uid
    farmer_obj = getattr(uid, 'farmer', None)
    
    # Active Listings
    approved_count = crop.objects.filter(user=uid, is_approved=True).count()
    
    # Crops Sold & Total Revenue
    sold_items = OrderItem.objects.filter(crop__user=uid, order__status__in=['Confirmed', 'Shipped', 'Delivered'])
    crops_sold_count = sold_items.count()
    total_revenue = sold_items.aggregate(Sum('subtotal'))['subtotal__sum'] or 0
    
    # Format total revenue beautifully
    if total_revenue >= 10000000:
        formatted_revenue = f"₹{total_revenue/10000000:.1f}Cr"
    elif total_revenue >= 100000:
        formatted_revenue = f"₹{total_revenue/100000:.1f}L"
    elif total_revenue >= 1000:
        formatted_revenue = f"₹{total_revenue/1000:.1f}K"
    else:
        formatted_revenue = f"₹{int(total_revenue)}"

    context = {
        'uid': uid, 
        'farmer': farmer_obj, 
        'approved_count': approved_count,
        'crops_sold_count': crops_sold_count,
        'formatted_revenue': formatted_revenue
    }

    if request.method == 'POST':
        action = request.POST.get('action', 'personal')
        if action == 'personal':
            uid.name = request.POST.get('name', uid.name)
            uid.email = request.POST.get('email', uid.email)
            uid.city = request.POST.get('city', uid.city)
            uid.save()
        elif action == 'farm' and farmer_obj:
            farmer_obj.farm_name = request.POST.get('farm_name', farmer_obj.farm_name)
            farmer_obj.acres = request.POST.get('acres', farmer_obj.acres) or None
            farmer_obj.address = request.POST.get('address', farmer_obj.address)
            if request.FILES.get('photo'):
                farmer_obj.photo = request.FILES['photo']
            farmer_obj.save()
        elif action == 'docs' and farmer_obj:
            farmer_obj.adharno = request.POST.get('adharno', farmer_obj.adharno)
            if request.FILES.get('adharcard'):
                farmer_obj.adharcard = request.FILES['adharcard']
            if request.FILES.get('pancard'):
                farmer_obj.pancard = request.FILES['pancard']
            if request.FILES.get('passbook'):
                farmer_obj.passbook = request.FILES['passbook']
            if request.FILES.get('seventwel'):
                farmer_obj.seventwel = request.FILES['seventwel']
            # Reset permission after successful update
            farmer_obj.doc_edit_permission = False
            farmer_obj.save()
        elif action == 'notif' and farmer_obj:
            farmer_obj.notif_new_order = request.POST.get('notif_new_order') == 'on'
            farmer_obj.notif_price_alerts = request.POST.get('notif_price_alerts') == 'on'
            farmer_obj.notif_blog = request.POST.get('notif_blog') == 'on'
            farmer_obj.notif_sms = request.POST.get('notif_sms') == 'on'
            farmer_obj.notif_gov_schemes = request.POST.get('notif_gov_schemes') == 'on'
            farmer_obj.save()
        elif action == 'delete_account':
            uid.delete()
            messages.success(request, 'Your account has been permanently deleted.')
            return redirect('login')
            
        messages.success(request, 'Profile updated successfully!')
        return redirect('farmer_profile')

    return render(request, "farmer/profile.html", context)

@check_login(['Farmer'])
def govt_info(request):
    all_info = gov_info.objects.all().order_by('-created_at')
    context = {'all_info': all_info}
    if request.method == "POST":
        state = request.POST.get('state')
        if state == "Central":
            return redirect('gov_info')
        elif state == "Central Government":
            all_info = gov_info.objects.filter(state="Central Government").order_by('-created_at')
            context = {'all_info': all_info}
        else:
            all_info = gov_info.objects.filter(state__in=["Central Government", state]).order_by('-created_at')
            context = {'all_info': all_info}
        return render(request, "farmer/gov_info.html",context)
    return render(request, "farmer/gov_info.html",context)

@check_login(['Farmer'])
def farmer_chatbot(request):
    uid = request.uid
    room = chatroom.objects.filter(user=uid).first()
    if not room:
        room = chatroom.objects.create(user=uid)

    if request.method == "POST":
        sender = User.objects.get(id=uid.id)
        question = request.POST.get('Question')
        name = uid.name  

        API_KEY = "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"

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        MODEL = "openai/gpt-oss-20b:free"

        data = {
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": f"""
                You are Krushi Mitra AI , a smart farming assistant.

                User Details:
                - Name: {name}

                Rules:
                - always be friendly
                - if user ask than always give price of 20kg of user asked crop
                - dont answer the quesions other than farming,farming tools..etc
                - creator of model : Jeel Tank
                - Always call user by name
                - Answer in language user want
                - Keep answers short
                - Format response using HTML tags like <b>, <ul>, <li>, <br>
                - Do NOT use markdown (** or -)
                """
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            "stream": True
        }

        answer = ""
        message.objects.create(
        chat_room=room,
        role="user",
        content=question
        )
        try:
            response = requests.post(url, headers=headers, json=data, stream=True)

            if response.status_code != 200:
                answer = f"Error: {response.text}"
            else:
                for line in response.iter_lines():
                    if line:
                        decoded = line.decode("utf-8")

                        if decoded.startswith("data: "):
                            chunk = decoded.replace("data: ", "")

                            if chunk == "[DONE]":
                                break

                            try:
                                json_data = json.loads(chunk)
                                content = json_data['choices'][0]['delta'].get('content', '')
                                answer += content
                            except:
                                pass

        except Exception as e:
            answer = f"Network Error: {str(e)}"
        
        message.objects.create(
            chat_room=room,
            role="ai",
            content=answer
        )
        
        all_messages = room.messages.all().order_by('created_at')
        context = {
            "uid": uid,
            "messages": all_messages,
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                "status": "success",
                "bot_message": answer
            })

        return render(request, "farmer/chatbot.html", context)
    all_messages = room.messages.all().order_by('created_at')
    context = {
            "uid": uid,
            "messages": all_messages,
        }
    return render(request, "farmer/chatbot.html", context)

@check_login(['Farmer'])
def clear_history(request):
    uid = request.uid
    room = chatroom.objects.filter(user=uid).first()
    if room:
        room.messages.all().delete()
    return redirect('farmer_chatbot')

@check_login(['Farmer'])
def community_chat(request):
    uid = request.uid
    all_messages = community_message.objects.all()
    all_users = User.objects.all()
    user_count = len([user for user in all_users if user.is_active])
    member_count = len([user for user in all_users if user.role == 'Farmer'])
    context = {'uid': uid, 'messages':  all_messages, 'user_count': user_count, 'member_count': member_count}
    if request.method == "POST":
        sender = User.objects.get(id = uid.id)
        # message_content = request.POST.get('message')
        message_content = request.POST['message']
        if len(message_content) <= 0:
            messages.error(request, "Message cannot be empty")
            return render(request, "farmer/community_chat.html", context)
        else:
            user_message = community_message.objects.create(
                    sender=sender,
                    message=message_content,
            )
            try:
                image= request.FILES.get('image')
                is_image = True
            except:
                is_image = False

            if is_image:
                user_message.image = image
            user_message.save()
            return redirect('community_chat')
    return render(request, "farmer/community_chat.html", context)


def community_chat_delet(request,pk):
    community_message.objects.filter(id=pk).delete()
    return redirect('community_chat')

def predict_price(price, category, years, condition):

    years = max(years, 0)

    log_pred = price_model.predict([
        [category, years, condition]
    ])[0]

    rate = math.exp(log_pred)

    final_price = max(price * rate, price * 0.1)

    return round(final_price, 2)

@check_login(['Farmer'])
def tool_price(request):
    result = None

    if request.method == "POST":
        category = request.POST.get('category')
        condition = request.POST.get('condition')
        years = int(request.POST.get('years', 0))
        price = int(request.POST.get('price', 0))
        
        category_map = {"tractor": 0,"harvester": 1,"other": 2,"tools": 3,"hand": 4}

        condition_map = {"poor": 1,"average": 2,"good": 4,"excellent": 5}

        category_no = category_map.get(category, 0)
        condition_no = condition_map.get(condition, 2)

        result = predict_price(price, category_no, years, condition_no)

        context = {'category': category,'condition': condition,'years': years,'price': price,'result': result}

        return render(request, "farmer/tool_price.html", context)

    return render(request, "farmer/tool_price.html")

def add_tool(request):
    uid = request.uid if hasattr(request, 'uid') else None
    return render(request, "farmer/add_tool.html", {'uid': uid})

@check_login(['Farmer'])
def delete_crop(request, pk):
    uid = request.uid
    crop_obj = crop.objects.filter(id=pk, user=uid).first()
    if crop_obj:
        crop_obj.delete()
        messages.success(request, 'Crop deleted successfully.')
    else:
        messages.error(request, 'Crop not found.')
    return redirect('farmer_crops')

@check_login(['Farmer'])
def edit_crop(request, pk):
    uid = request.uid
    crop_obj = crop.objects.filter(id=pk, user=uid).first()
    if not crop_obj:
        messages.error(request, 'Crop not found.')
        return redirect('farmer_crops')

    if request.method == 'POST':
        crop_obj.cropname = request.POST.get('cropname', crop_obj.cropname)
        crop_obj.category = request.POST.get('category', crop_obj.category)
        crop_obj.quantity = request.POST.get('quantity', crop_obj.quantity)
        crop_obj.price = request.POST.get('price', crop_obj.price)
        crop_obj.description = request.POST.get('description', crop_obj.description)
        if request.FILES.get('image'):
            crop_obj.image = request.FILES['image']
        crop_obj.save()
        messages.success(request, 'Crop updated successfully!')
        return redirect('farmer_crops')

    # For GET requests redirect back (we use inline modal)
    return redirect('farmer_crops')

def rain_probability(temperature,humidity,wind_speed,clouds):
    BASE_DIR = Path(__file__).resolve().parent
    csv_path = BASE_DIR / "data" / "weather_prediction.csv"
    df = pd.read_csv(csv_path)

    X = df[["temperature", "humidity", "wind_speed", "clouds"]]
    y = df["rain"]

    model = RandomForestClassifier(
    n_estimators=200,
    random_state=42)

    model.fit(X, y)
    result = model.predict_proba([
        [temperature, humidity, wind_speed, clouds]
    ])
    return round(result[0][1] * 100)

@check_login(['Farmer'])
def farmer_news(request):
    api_key = "cda9b54ada6d720cbc78948d2e86b4d8"
    uid = request.uid
    city = uid.city if uid.city else "Delhi"
    all_news = news.objects.all().order_by('-created_at')

    cache_key = f"weather_{city}"

    data = cache.get(cache_key)
    if data is None:
        response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        )
        data = response.json()
        cache.set(cache_key, data, 600)

    temperature = round(data["main"]["temp"])
    condition = data["weather"][0]["main"]
    humidity = data["main"]["humidity"]
    wind_speed = round(data["wind"]["speed"]*3.6)
    clouds = data["clouds"]["all"]

    rain = rain_probability(
        temperature,
        humidity,
        wind_speed,
        clouds
    )

    if request.method == "POST":
        state = request.POST.get('state')
        if state: 
            state = state.capitalize()
            all_news = all_news.filter(state=state)
            
        category = request.POST.get('category')
        if category:
            all_news = all_news.filter(category=category)
            
        search_date = request.POST.get('date')
        if search_date:
            all_news = all_news.filter(created_at__date=search_date)

        print(all_news)
        context = {
        'all_news': all_news,
        "city": city.upper(),
        "temperature": temperature,
        "condition": condition,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "rain_probability": rain
        }
        return render(request, "farmer/news.html", context)

    context = {'all_news': all_news,"city": city.upper(),"temperature": temperature,"condition": condition,"humidity": humidity,"wind_speed": wind_speed,"rain_probability": rain}
    return render(request, "farmer/news.html", context)


#++++++++++++++++++++++==============================+++++++++++++++++++++===========================++++++++++++++++++++++++++++=====================

# ─────────────────────────────────────────────────────────────────────────────
#  FARMER TOOL CRUD
# ─────────────────────────────────────────────────────────────────────────────

def _tool_predicted_price(category_str, condition_str, years, original_price):
    """
    Re-uses the predict_price() ML function from this file.
    Returns a rounded integer rental price estimate, or None on error.
    """
    category_map  = {"tractor": 0, "harvester": 1, "other": 2, "tools": 3, "hand": 4}
    condition_map = {"poor": 5, "average": 4, "good": 3, "excellent": 2}
    try:
        cat  = category_map.get(category_str, 0)
        cond = condition_map.get(condition_str, 3)
        return int(predict_price(original_price, cat, int(years), cond))
    except Exception:
        return None


@check_login(['Farmer'])
def my_tool_list(request):
    uid = request.uid
    qs  = FarmerTool.objects.filter(user=uid).order_by('-created_at')

    # Search & filter
    search   = request.GET.get('search', '').strip()
    category = request.GET.get('category', '')
    status   = request.GET.get('status', '')
    if search:
        qs = qs.filter(tool_name__icontains=search)
    if category:
        qs = qs.filter(category=category)
    if status:
        qs = qs.filter(availability_status=status)

    # Attach predicted price to each tool
    tools_with_price = []
    for t in qs:
        predicted = t.predicted_price
        if predicted is None:
            predicted = _tool_predicted_price(t.category, t.condition, t.years_used, t.original_price)
            t.predicted_price = predicted
            t.save(update_fields=['predicted_price'])
        tools_with_price.append({'tool': t, 'predicted_price': predicted})

    context = {
        'uid': uid,
        'tools_with_price': tools_with_price,
        'search': search,
        'selected_category': category,
        'selected_status': status,
        'total': qs.count(),
    }
    return render(request, 'farmer/my_tools.html', context)


@check_login(['Farmer'])
def tool_add(request):
    uid = request.uid
    if request.method == 'POST':
        tool_name          = request.POST.get('tool_name', '').strip()
        category           = request.POST.get('category', '')
        company            = request.POST.get('company', '').strip()
        model_name         = request.POST.get('model_name', '').strip()
        manufacturing_year = request.POST.get('manufacturing_year', '')
        horsepower         = request.POST.get('horsepower', '') or None
        condition          = request.POST.get('condition', '')
        description        = request.POST.get('description', '').strip()
        availability_status= request.POST.get('availability_status', 'available')
        location           = request.POST.get('location', '').strip()
        original_price     = request.POST.get('original_price', 0)
        years_used         = request.POST.get('years_used', 0)
        image              = request.FILES.get('image')

        errors = {}
        if not tool_name:        errors['tool_name'] = 'Tool name is required.'
        if not category:         errors['category']  = 'Category is required.'
        if not condition:        errors['condition'] = 'Condition is required.'
        if not original_price:   errors['original_price'] = 'Purchase price is required.'

        if manufacturing_year:
            try:
                yr = int(manufacturing_year)
                from datetime import datetime
                if yr < 1900 or yr > datetime.now().year:
                    errors['manufacturing_year'] = 'Enter a valid manufacturing year.'
            except ValueError:
                errors['manufacturing_year'] = 'Enter a valid year.'

        if errors:
            context = {
                'uid': uid, 'errors': errors,
                'post': request.POST,
            }
            return render(request, 'farmer/tool_add.html', context)

        predicted_val = _tool_predicted_price(category, condition, int(years_used) if years_used else 0, int(original_price))

        t = FarmerTool.objects.create(
            user=uid,
            tool_name=tool_name,
            category=category,
            company=company or None,
            model_name=model_name or None,
            manufacturing_year=int(manufacturing_year) if manufacturing_year else None,
            horsepower=int(horsepower) if horsepower else None,
            condition=condition,
            description=description or None,
            availability_status=availability_status,
            location=location or None,
            original_price=int(original_price),
            predicted_price=predicted_val,
            years_used=int(years_used) if years_used else 0,
        )
        if image:
            t.image = image
            t.save()
        messages.success(request, f'Tool "{tool_name}" added successfully! Predicted selling price: ₹{predicted_val}')
        return redirect('my_tool_list')

    return render(request, 'farmer/tool_add.html', {'uid': uid})


@check_login(['Farmer'])
def tool_edit(request, pk):
    uid      = request.uid
    tool_obj = FarmerTool.objects.filter(id=pk, user=uid).first()
    if not tool_obj:
        messages.error(request, 'Tool not found or access denied.')
        return redirect('my_tool_list')

    predicted = _tool_predicted_price(tool_obj.category, tool_obj.condition, tool_obj.years_used, tool_obj.original_price)

    if request.method == 'POST':
        tool_obj.tool_name           = request.POST.get('tool_name', tool_obj.tool_name).strip()
        tool_obj.category            = request.POST.get('category', tool_obj.category)
        tool_obj.company             = request.POST.get('company', '').strip() or None
        tool_obj.model_name          = request.POST.get('model_name', '').strip() or None
        yr = request.POST.get('manufacturing_year', '')
        tool_obj.manufacturing_year  = int(yr) if yr else None
        hp = request.POST.get('horsepower', '')
        tool_obj.horsepower          = int(hp) if hp else None
        tool_obj.condition           = request.POST.get('condition', tool_obj.condition)
        tool_obj.description         = request.POST.get('description', '').strip() or None
        tool_obj.availability_status = request.POST.get('availability_status', tool_obj.availability_status)
        tool_obj.location            = request.POST.get('location', '').strip() or None
        tool_obj.original_price      = int(request.POST.get('original_price', tool_obj.original_price))
        tool_obj.years_used          = int(request.POST.get('years_used', 0))
        predicted = _tool_predicted_price(tool_obj.category, tool_obj.condition, tool_obj.years_used, tool_obj.original_price)
        tool_obj.predicted_price = predicted

        if request.FILES.get('image'):
            tool_obj.image = request.FILES['image']
        tool_obj.save()
        messages.success(request, 'Tool updated successfully!')
        return redirect('my_tool_list')

    context = {'uid': uid, 'tool': tool_obj, 'predicted': predicted}
    return render(request, 'farmer/tool_edit.html', context)


@check_login(['Farmer'])
def tool_detail(request, pk):
    uid      = request.uid
    tool_obj = FarmerTool.objects.filter(id=pk, user=uid).first()
    if not tool_obj:
        messages.error(request, 'Tool not found or access denied.')
        return redirect('my_tool_list')
    predicted = tool_obj.predicted_price
    if predicted is None:
        predicted = _tool_predicted_price(tool_obj.category, tool_obj.condition, tool_obj.years_used, tool_obj.original_price)
        tool_obj.predicted_price = predicted
        tool_obj.save(update_fields=['predicted_price'])
    context   = {'uid': uid, 'tool': tool_obj, 'predicted': predicted}
    return render(request, 'farmer/tool_detail.html', context)


@check_login(['Farmer'])
def tool_delete(request, pk):
    uid      = request.uid
    tool_obj = FarmerTool.objects.filter(id=pk, user=uid).first()
    if tool_obj:
        name = tool_obj.tool_name
        tool_obj.delete()
        messages.success(request, f'Tool "{name}" deleted successfully.')
    else:
        messages.error(request, 'Tool not found.')
    return redirect('my_tool_list')


@check_login(['Farmer'])
def get_tool_price_api(request):
    """AJAX endpoint: returns predicted rental price JSON."""
    category       = request.GET.get('category', '')
    condition      = request.GET.get('condition', '')
    years_used     = request.GET.get('years_used', 0)
    original_price = request.GET.get('original_price', 0)
    try:
        predicted = _tool_predicted_price(category, condition, int(years_used), int(original_price))
        if predicted is not None:
            return JsonResponse({'status': 'ok', 'price': predicted})
        return JsonResponse({'status': 'not_found', 'price': None})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
