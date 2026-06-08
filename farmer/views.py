from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import * 
import requests , math ,json,sseclient
from django.contrib.auth.decorators import login_required
from sklearn.linear_model import LinearRegression 
from sklearn.ensemble import RandomForestClassifier

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
                Buyer.objects.create(user=user, adharno=aadhar, gst_no=gst)
                
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

@check_login(['Farmer'])
def farmer_home(request):
    return render(request, "farmer/home.html")

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
    return render(request, "farmer/tools.html")

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
    return render(request, "farmer/profile.html")

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
        
        MODEL = "z-ai/glm-4.5-air:free"

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
                - if user ask than always give price of 20kg of any crop
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
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++MESSAGE : " , message_content)

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
        return render(request, "farmer/community_chat.html", context)
    return render(request, "farmer/community_chat.html", context)

def predict_price(price, category, years, condition):

    years = min(years, 5)

    X = [
        [0, 1, 5],
        [0, 3, 4],
        [1, 2, 3],
        [1, 4, 2],
        [2, 2, 4],
        [2, 5, 2],
        [3, 1, 4],
        [3, 3, 3],
        [4, 1, 5],
        [4, 2, 3]
    ]

    y = [0.90, 0.75, 0.70, 0.55, 0.80, 0.60, 0.85, 0.65, 0.90, 0.70]

    log_y = [math.log(v) for v in y]

    model = LinearRegression()
    model.fit(X, log_y)

    log_pred = model.predict([
        [category, years, condition]
    ])[0]

    print("LOG PRED :", log_pred)

    rate = math.exp(log_pred)

    print("RATE :", rate)

    final_price = price * rate

    # minimum protection
    final_price = max(final_price, price * 0.1)

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

        condition_map = {"poor": 5,"average": 4,"good": 3,"excellent": 2}

        category_no = category_map.get(category, 0)
        condition_no = condition_map.get(condition, 3)

        result = predict_price(price, category_no, years, condition_no)

        context = {'category': category,'condition': condition,'years': years,'price': price,'result': result}

        return render(request, "farmer/tool_price.html", context)

    return render(request, "farmer/tool_price.html")

def add_tool(request):
    return render(request, "farmer/add_tool.html")

def rain_probability(temperature,humidity,wind_speed,clouds):
    model = RandomForestClassifier()
    
    X = [
        [45,20,5,5],
        [44,22,6,10],
        [43,25,8,15],
        [42,28,10,20],
        [41,30,12,25],
        [40,35,14,30],
        [39,40,16,35],
        [38,45,18,40],
        [37,50,20,45],
        [36,55,22,50],
        [35,60,24,55],
        [34,65,20,60],
        [33,70,18,65],
        [32,75,16,70],
        [31,80,14,75],
        [30,85,12,80],
        [29,90,10,85],
        [28,92,8,90],
        [27,95,6,95],
        [26,98,5,100],
        [35,72,18,68],
        [34,74,16,72],
        [33,78,15,78],
        [32,82,14,82],
        [31,86,12,86],
        [30,88,10,88],
        [29,91,9,92],
        [28,94,8,95],
        [27,96,7,97],
        [26,99,6,100]
    ]

    y = [
        0,0,0,0,0,
        0,0,0,0,0,
        0,1,1,1,1,
        1,1,1,1,1,
        1,1,1,1,1,
        1,1,1,1,1
    ] # 1 is rain, 0 is no rain
    model.fit(X, y)
    result = model.predict_proba([
        [temperature, humidity, wind_speed, clouds]
    ])
    return round(result[0][1] * 100)

@check_login(['Farmer'])
def farmer_news(request):
    # api_key = "cda9b54ada6d720cbc78948d2e86b4d8"
    uid = request.uid
    city = uid.city if uid.city else "Delhi"
    all_news = news.objects.all().order_by('-created_at')

    # response= requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
    # data = response.json()
    # print("WEATHER DATA :", data)
    # temperature = round(data["main"]["temp"])
    # condition = data["weather"][0]["main"]
    # humidity = data["main"]["humidity"]
    # wind_speed = round(data["wind"]["speed"]*3.6)
    # clouds = data["clouds"]["all"]
    # 
    temperature = 10
    condition = "Rainy"
    humidity = 90
    wind_speed = 10
    clouds = 90
    if request.method == "POST":
        state = request.POST.get('state').capitalize()
        category = request.POST.get('category')
        print("FILTERS :", category)
        if state and category:
            all_news = news.objects.filter(state=state, category=category , is_breaking=True).order_by('-created_at')
        elif state:
            all_news = news.objects.filter(state=state,is_breaking=True).order_by('-created_at')
        elif category:
            all_news = news.objects.filter(category=category,is_breaking=True).order_by('-created_at')

        print(all_news)
        context = {
        'all_news': all_news,
        "city": city.upper(),
        "temperature": temperature,
        "condition": condition,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "rain_probability": rain_probability(temperature, humidity, wind_speed, clouds)
        }
        return render(request, "farmer/news.html", context)

    context = {'all_news': all_news,"city": city.upper(),"temperature": temperature,"condition": condition,"humidity": humidity,"wind_speed": wind_speed,"rain_probability": rain_probability(temperature, humidity, wind_speed, clouds)}
    return render(request, "farmer/news.html", context)


#++++++++++++++++++++++==============================+++++++++++++++++++++===========================++++++++++++++++++++++++++++=====================

@check_login(['Buyer'])
def buyer_home(request):
        return render(request, "buyer/home.html")

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