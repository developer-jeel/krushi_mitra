import random
import string
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from farmer.models import (
    User, Farmer, crop, chatroom, message, bloag,
    community_message, gov_info, news, FarmerTool,
    farmer_premium_plans, farmer_selling_limit,
    premium_buyer as farmer_premium_buyer, farmer_premium_history
)
from buyer.models import (
    Buyer, bank_details, verification_details, premium_plans,
    premium_buyer, premium_history, premium_coupon, discount_coupon,
    Cart, CartItem, Order, OrderItem, notifications, saved,
    exportinquiry, bulkrequest
)


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS & REALISTIC DATA CATALOGS
# ─────────────────────────────────────────────────────────────────────────────

MALE_NAMES = [
    "Rajesh", "Ramesh", "Amit", "Suresh", "Vijay", "Anil", "Patel", "Vikram", "Sanjay",
    "Deepak", "Dharmendra", "Paresh", "Bhavesh", "Hitesh", "Jignesh", "Nilesh", "Pankaj",
    "Chetan", "Hardik", "Tushar", "Snehal", "Aniket", "Rahul", "Gaurav", "Manish",
    "Kishore", "Mayur", "Pratik", "Kiran", "Ashok", "Ketan", "Siddharth", "Yash", "Jay",
    "Devendra", "Ghanshyam", "Kalyan", "Mansukh", "Raghav", "Vrajesh", "Parag"
]

FEMALE_NAMES = [
    "Priya", "Anjali", "Pooja", "Neha", "Ritu", "Sunita", "Geeta", "Rekha", "Anita",
    "Meena", "Swati", "Kavita", "Dipti", "Shilpa", "Bhavna", "Nita", "Hetel", "Komal",
    "Rutuja", "Shweta", "Payal", "Vimla", "Kiran", "Pinky", "Monika", "Aarti", "Saroj"
]

SURNAMES = [
    "Patel", "Sharma", "Verma", "Singh", "Joshi", "Mehta", "Shah", "Chaudhary",
    "Rathod", "Jadeja", "Parmar", "Solanki", "Zala", "Desai", "Trivedi", "Bhatt",
    "Gohil", "Chauhan", "Yadav", "Gupta", "Vaghela", "Makwana", "Dabhi", "Koli",
    "Thakor", "Gajera", "Kheni", "Vora", "Savani", "Bhalani", "Kakadiya", "Sojitra"
]

GUJARAT_CITIES = [
    "Rajkot", "Ahmedabad", "Surat", "Vadodara", "Junagadh", "Amreli", "Jamnagar",
    "Bhavnagar", "Anand", "Mehsana", "Gandhinagar", "Patan", "Banaskantha",
    "Sabarkantha", "Kutch", "Porbandar", "Navsari", "Valsad", "Bharuch", "Kheda",
    "Surendranagar", "Morbi", "Dahod", "Panchmahal", "Tapi", "Gir Somnath", "Botad"
]

STATES = [
    "Gujarat", "Gujarat", "Gujarat", "Gujarat", "Maharashtra", "Rajasthan",
    "Punjab", "Haryana", "Madhya Pradesh", "Uttar Pradesh"
]

BUSINESS_TYPES = [
    "Wholesaler", "Retailer", "Exporter", "Food Processor", "Mandi Trader",
    "Agri Distributer", "Supermarket Supplier", "Commission Agent"
]

CROPS_CATALOG = [
    {"name": "Wheat", "cat": "grain cereals", "min_p": 24, "max_p": 40, "desc": "High grade Sharbati & Lokwan wheat directly from farms."},
    {"name": "Rice", "cat": "grain cereals", "min_p": 38, "max_p": 90, "desc": "Premium quality aromatic Basmati and Non-Basmati rice."},
    {"name": "Maize", "cat": "grain cereals", "min_p": 18, "max_p": 28, "desc": "Yellow feed quality and sweet corn maize."},
    {"name": "Bajra", "cat": "grain cereals", "min_p": 20, "max_p": 32, "desc": "Organic hybrid Bajra grains ideal for flour mills."},
    {"name": "Cotton", "cat": "cotton", "min_p": 68, "max_p": 115, "desc": "Long staple raw Shankar-6 cotton bales."},
    {"name": "Groundnut", "cat": "pulses", "min_p": 62, "max_p": 98, "desc": "Bold Bold-size Bold peanuts with high oil content."},
    {"name": "Soybean", "cat": "pulses", "min_p": 44, "max_p": 72, "desc": "Non-GMO yellow soybean seeds for oil extraction."},
    {"name": "Mustard", "cat": "spices", "min_p": 55, "max_p": 85, "desc": "Black and yellow mustard seeds with high pungency."},
    {"name": "Castor", "cat": "spices", "min_p": 58, "max_p": 92, "desc": "Clean Gujarat castor seeds for industrial oil mills."},
    {"name": "Chickpea", "cat": "pulses", "min_p": 52, "max_p": 88, "desc": "Desi Chana and Dollar Kabuli Chana varieties."},
    {"name": "Green Gram", "cat": "pulses", "min_p": 76, "max_p": 125, "desc": "Clean polished Moong whole grains."},
    {"name": "Black Gram", "cat": "pulses", "min_p": 72, "max_p": 118, "desc": "Bold Urad whole seeds harvested fresh."},
    {"name": "Onion", "cat": "vegetables", "min_p": 16, "max_p": 46, "desc": "Red Mahuva & Nasik quality export onions."},
    {"name": "Potato", "cat": "vegetables", "min_p": 14, "max_p": 36, "desc": "Deesa Cold storage Jyoti & LR potatoes."},
    {"name": "Tomato", "cat": "vegetables", "min_p": 18, "max_p": 52, "desc": "Fresh firm red farm tomatoes."},
    {"name": "Cumin", "cat": "spices", "min_p": 220, "max_p": 380, "desc": "Premium Unjha Jeera with rich aroma & 99% purity."},
    {"name": "Coriander", "cat": "spices", "min_p": 82, "max_p": 150, "desc": "Green Eagle quality Dhana seeds."}
]

TOOL_CATALOG = [
    {"name": "Mahindra 575 DI Tractor", "cat": "tractor", "company": "Mahindra", "model": "575 DI", "hp": 45, "orig": 720000, "pred": 480000},
    {"name": "John Deere 5050 D Tractor", "cat": "tractor", "company": "John Deere", "model": "5050 D", "hp": 50, "orig": 850000, "pred": 590000},
    {"name": "Swaraj 744 FE Tractor", "cat": "tractor", "company": "Swaraj", "model": "744 FE", "hp": 48, "orig": 780000, "pred": 510000},
    {"name": "Kubota Neostar Harvester", "cat": "harvester", "company": "Kubota", "model": "Harvester 868", "hp": 70, "orig": 1800000, "pred": 1250000},
    {"name": "Fieldking Rotary Tiller", "cat": "tools", "company": "Fieldking", "model": "FKR-2023", "hp": 35, "orig": 120000, "pred": 82000},
    {"name": "Lemken Hydraulic Reversible Plough", "cat": "tools", "company": "Lemken", "model": "Opal 080", "hp": 45, "orig": 210000, "pred": 145000},
    {"name": "Aspee Heavy Duty Power Sprayer", "cat": "tools", "company": "Aspee", "model": "PS-500", "hp": 5, "orig": 35000, "pred": 22000},
    {"name": "Manual Seed Drill Machine", "cat": "hand", "company": "National Agri", "model": "SD-9", "hp": 0, "orig": 18000, "pred": 11000}
]

EXPORT_COUNTRIES = [
    "UAE", "Saudi Arabia", "Singapore", "Nepal", "Bangladesh", "Malaysia", "Sri Lanka"
]

PACKAGING_TYPES = [
    "Jute Bag 50kg", "HDPE Bag 25kg", "PP Woven Bag 50kg", "Bulk Container 20ft"
]

QUALITY_STANDARDS = [
    "AGMARK Grade A", "Export Grade 1", "ISO 22000 Certified", "Organic Certified"
]

PORTS = [
    "Mundra Port, Gujarat", "Kandla Port, Gujarat", "Jawaharlal Nehru Port, Mumbai", "Hazira Port, Surat"
]

PAYMENT_METHODS = ["UPI / QR", "Credit / Debit Card", "Net Banking", "Wallet"]
ORDER_STATUSES = ["Delivered", "Delivered", "Delivered", "Confirmed", "Shipped", "Pending", "Cancelled"]
PAYMENT_STATUSES = ["Paid", "Paid", "Paid", "Pending", "Failed", "Refunded"]

BANKS = ["State Bank of India", "HDFC Bank", "ICICI Bank", "Bank of Baroda", "Axis Bank", "Punjab National Bank"]

COMMUNITY_TOPICS = [
    "What is the best fertilizer combination for Groundnut in Saurashtra region?",
    "How to control pink bollworm in Shankar-6 Cotton crop effectively?",
    "Unjha Jeera market price predictions for upcoming harvest season.",
    "Is micro-drip irrigation helpful for Onion farming in Dhoraji?",
    "Experience with organic Jeevamrut on Sharbati Wheat productivity.",
    "Government subsidy approval timeline for Solar Pump Installation 2026."
]

AI_CONVERSATIONS = [
    ("user", "Suggest the best high-yield Wheat variety for Gujarat soil."),
    ("ai", "For Gujarat soil and climate, Lokwan and GW-322 Sharbati wheat are highly recommended. Ensure 3-4 irrigations and balanced NPK fertilizer (120:60:40)."),
    ("user", "How to identify yellow mosaic virus in Green Gram?"),
    ("ai", "Yellow mosaic virus causes yellow spots on leaves. Control whitefly vectors using Neem oil (10,000 PPM) or Imidacloprid spray immediately."),
    ("user", "What is the expected market price for Cumin in Unjha मंडी?"),
    ("ai", "Cumin prices in Unjha are currently trading between ₹260 - ₹340 per kg due to high export demand in Gulf countries.")
]


class Command(BaseCommand):
    help = "Seeds the entire Krushi Mitra database with realistic, production-ready agriculture data across all models."

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Reset existing generated dummy data before seeding')
        parser.add_argument('--users', type=int, default=500, help='Total users to seed (default: 500)')
        parser.add_argument('--crops', type=int, default=600, help='Crop listings to seed (default: 600)')
        parser.add_argument('--orders', type=int, default=3000, help='Orders to seed across last 12 months (default: 3000)')

    def handle(self, *args, **options):
        reset = options['reset']
        total_user_count = options['users']
        num_crops_count = options['crops']
        num_orders_count = options['orders']

        self.stdout.write(self.style.MIGRATE_HEADING("=== Krushi Mitra Full Database Seeder ==="))

        if reset:
            self.stdout.write(self.style.WARNING("Reset flag provided. Purging existing dummy data..."))
            with transaction.atomic():
                dummy_users = User.objects.filter(username__startswith='dummy_')
                dummy_cnt = dummy_users.count()
                dummy_users.delete()

                # Clean standalone models
                gov_info.objects.all().delete()
                news.objects.all().delete()
                premium_coupon.objects.all().delete()
                discount_coupon.objects.all().delete()
                farmer_premium_plans.objects.all().delete()
                premium_plans.objects.all().delete()
                bloag.objects.all().delete()

                self.stdout.write(self.style.SUCCESS(f"Cleaned up {dummy_cnt} dummy user accounts and related records."))

        password_hash = make_password('password123')
        now = timezone.now()

        # ─────────────────────────────────────────────────────────────────────
        # 0. INITIALIZE PLANS & COUPONS
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n[0/12] Initializing Default Plans & Coupons..."))

        buyer_p, _ = premium_plans.objects.get_or_create(defaults={'standard_price': 99, 'premium_price': 199, 'year_dis': 20})
        farmer_p, _ = farmer_premium_plans.objects.get_or_create(defaults={'standard_price': 99, 'premium_price': 199, 'year_dis': 20})

        premium_coupon.objects.get_or_create(code="WELCOME50", defaults={
            'discount_type': 'percent', 'discount_value': 50.00, 'label': '50% Off Welcome Offer',
            'minimum_amount': 99, 'usage_limit': 1000, 'used_count': 142, 'expiry_date': now + timedelta(days=90)
        })
        premium_coupon.objects.get_or_create(code="PREMIUM100", defaults={
            'discount_type': 'flat', 'discount_value': 100.00, 'label': 'Flat ₹100 Discount',
            'minimum_amount': 500, 'usage_limit': 500, 'used_count': 88, 'expiry_date': now + timedelta(days=60)
        })

        discount_coupon.objects.get_or_create(code="KRUSHI20", defaults={
            'discount_type': 'percent', 'discount_value': 20.00, 'label': '20% Off Crop Order',
            'minimum_amount': 500, 'usage_limit': 2000, 'used_count': 320, 'expiry_date': now + timedelta(days=120)
        })
        discount_coupon.objects.get_or_create(code="FLAT200", defaults={
            'discount_type': 'flat', 'discount_value': 200.00, 'label': 'Flat ₹200 Off Bulk Order',
            'minimum_amount': 2000, 'usage_limit': 500, 'used_count': 64, 'expiry_date': now + timedelta(days=45)
        })

        self.stdout.write(self.style.SUCCESS("  Configured Premium Plans and Promo Coupons."))

        # ─────────────────────────────────────────────────────────────────────
        # 1. CREATE USERS & PROFILES (FARMERS + BUYERS)
        # ─────────────────────────────────────────────────────────────────────
        num_farmers = int(total_user_count * 0.65)
        num_buyers = total_user_count - num_farmers

        self.stdout.write(self.style.MIGRATE_HEADING(f"\n[1/12] Generating {num_farmers} Farmers and {num_buyers} Buyers..."))

        existing_contacts = set(User.objects.values_list('contact', flat=True))
        existing_emails = set(User.objects.values_list('email', flat=True))
        existing_adhars = set(Farmer.objects.values_list('adharno', flat=True))
        existing_gst = set(Buyer.objects.values_list('gst_no', flat=True))

        contact_seq = 9200000000
        adhar_seq = 300000000000
        gst_seq = 2000

        farmer_users_to_create = []
        farmer_meta = []

        # Farmers
        for i in range(num_farmers):
            first = random.choice(MALE_NAMES if i % 2 == 0 else FEMALE_NAMES)
            last = random.choice(SURNAMES)
            full_name = f"{first} {last}"
            username = f"dummy_farmer_{i+1}_{random.randint(1000,9999)}"

            while str(contact_seq) in existing_contacts:
                contact_seq += 1
            contact = str(contact_seq)
            existing_contacts.add(contact)
            contact_seq += 1

            email = f"farmer_{i+1}_{random.randint(100,999)}@krushimitra.in"
            if email in existing_emails:
                email = f"farmer_{i+1}_{random.randint(1000,9999)}@krushimitra.in"
            existing_emails.add(email)

            district = random.choice(GUJARAT_CITIES)
            joined_days = random.randint(1, 365)
            date_joined = now - timedelta(days=joined_days)

            user_obj = User(
                username=username,
                name=full_name,
                role='Farmer',
                email=email,
                city=district,
                contact=contact,
                password=password_hash,
                is_active=True,
                date_joined=date_joined
            )
            farmer_users_to_create.append(user_obj)

            while str(adhar_seq) in existing_adhars:
                adhar_seq += 1
            adhar = str(adhar_seq)
            existing_adhars.add(adhar)
            adhar_seq += 1

            farmer_meta.append({
                'farm_name': f"{last} Organic Farms",
                'acres': random.randint(4, 95),
                'address': f"Village {random.choice(['Jasdan', 'Gondal', 'Halvad', 'Dhoraji', 'Talaja', 'Paddhari'])}, Dist. {district}, Gujarat",
                'adharno': adhar,
                'date_joined': date_joined
            })

        created_farmer_users = User.objects.bulk_create(farmer_users_to_create)

        farmers_to_create = []
        farmer_limits = []
        farmer_prems = []
        farmer_hists = []

        for u_obj, meta in zip(created_farmer_users, farmer_meta):
            f_obj = Farmer(
                user=u_obj,
                farm_name=meta['farm_name'],
                acres=meta['acres'],
                address=meta['address'],
                adharno=meta['adharno']
            )
            farmers_to_create.append(f_obj)

        created_farmers = Farmer.objects.bulk_create(farmers_to_create)

        for f_obj in created_farmers:
            plan_choice = random.choices(['Free', 'Standard', 'Premium'], weights=[55, 30, 15])[0]
            cycle_choice = random.choice(['Monthly', 'Yearly'])
            limit_val = 1000 if plan_choice == 'Free' else (5000 if plan_choice == 'Standard' else 50000)

            farmer_limits.append(farmer_selling_limit(
                user=f_obj.user,
                total_sell_kg=random.randint(50, limit_val // 2),
                sellilimit=limit_val
            ))

            farmer_prems.append(farmer_premium_buyer(
                user=f_obj,
                premium_type=plan_choice,
                premium_time=cycle_choice,
                purchase_date=f_obj.user.date_joined
            ))

            if plan_choice != 'Free':
                price = 99 if plan_choice == 'Standard' else 199
                if cycle_choice == 'Yearly':
                    price = 950 if plan_choice == 'Standard' else 1910
                farmer_hists.append(farmer_premium_history(
                    user=f_obj,
                    plan=plan_choice,
                    billing_cycle=cycle_choice,
                    payment_method=random.choice(PAYMENT_METHODS),
                    price=price,
                    coupon_code=random.choice(['', 'FARMER10', 'WELCOME50']),
                    start_date=f_obj.user.date_joined
                ))

        farmer_selling_limit.objects.bulk_create(farmer_limits)
        farmer_premium_buyer.objects.bulk_create(farmer_prems)
        farmer_premium_history.objects.bulk_create(farmer_hists)

        # Buyers
        buyer_users_to_create = []
        buyer_meta = []

        for i in range(num_buyers):
            first = random.choice(MALE_NAMES if i % 2 == 1 else FEMALE_NAMES)
            last = random.choice(SURNAMES)
            full_name = f"{first} {last}"
            username = f"dummy_buyer_{i+1}_{random.randint(1000,9999)}"

            while str(contact_seq) in existing_contacts:
                contact_seq += 1
            contact = str(contact_seq)
            existing_contacts.add(contact)
            contact_seq += 1

            email = f"buyer_{i+1}_{random.randint(100,999)}@krushimitra.in"
            if email in existing_emails:
                email = f"buyer_{i+1}_{random.randint(1000,9999)}@krushimitra.in"
            existing_emails.add(email)

            district = random.choice(GUJARAT_CITIES)
            state = random.choice(STATES)
            joined_days = random.randint(1, 365)
            date_joined = now - timedelta(days=joined_days)

            user_obj = User(
                username=username,
                name=full_name,
                role='Buyer',
                email=email,
                city=district,
                contact=contact,
                password=password_hash,
                is_active=True,
                date_joined=date_joined
            )
            buyer_users_to_create.append(user_obj)

            gst_cand = f"24{last[:3].upper()}{gst_seq}1Z9"
            while gst_cand in existing_gst:
                gst_seq += 1
                gst_cand = f"24{last[:3].upper()}{gst_seq}1Z9"
            existing_gst.add(gst_cand)
            gst_seq += 1

            while str(adhar_seq) in existing_adhars:
                adhar_seq += 1
            adhar = str(adhar_seq)
            existing_adhars.add(adhar)
            adhar_seq += 1

            is_prem = random.choice([True, False, False])
            buyer_meta.append({
                'address': f"Plot {random.randint(10,500)}, Industrial Estate, {district}, {state}",
                'state': state,
                'pincode': str(random.randint(360001, 395010)),
                'business_type': random.choice(BUSINESS_TYPES),
                'gst_no': gst_cand,
                'is_verified': True,
                'is_premiume': is_prem,
                'adharno': adhar,
                'date_joined': date_joined
            })

        created_buyer_users = User.objects.bulk_create(buyer_users_to_create)

        buyers_to_create = []
        for u_obj, meta in zip(created_buyer_users, buyer_meta):
            buyers_to_create.append(Buyer(
                user=u_obj,
                address=meta['address'],
                state=meta['state'],
                pincode=meta['pincode'],
                business_type=meta['business_type'],
                gst_no=meta['gst_no'],
                is_verified=meta['is_verified'],
                is_premiume=meta['is_premiume']
            ))

        created_buyers = Buyer.objects.bulk_create(buyers_to_create)

        verifs = []
        banks = []
        carts = []
        buyer_prems = []
        buyer_hists = []

        for b_obj, meta in zip(created_buyers, buyer_meta):
            verifs.append(verification_details(
                user=b_obj,
                msme_no=f"UDYAM-GJ-{random.randint(10,99)}-{random.randint(10000,99999)}",
                trade_license=f"TL/{random.randint(2023,2026)}/{random.randint(1000,9999)}",
                adharno=meta['adharno']
            ))
            banks.append(bank_details(
                user=b_obj,
                pan_no=f"ABCDE{random.randint(1000,9999)}F",
                account_holder=b_obj.user.name,
                account_no=str(random.randint(1000000000, 9999999999)),
                ifsc_code=f"SBIN000{random.randint(1000,9999)}",
                bank_name=random.choice(BANKS)
            ))
            carts.append(Cart(user=b_obj.user, tax_per=5, cart_limit=50000 if meta['is_premiume'] else 5000))

            plan_choice = 'Premium' if meta['is_premiume'] else random.choice(['Free', 'Standard'])
            cycle_choice = random.choice(['Monthly', 'Yearly'])

            buyer_prems.append(premium_buyer(
                user=b_obj,
                premium_type=plan_choice,
                premium_time=cycle_choice,
                purchase_date=meta['date_joined']
            ))

            if plan_choice != 'Free':
                price = 99 if plan_choice == 'Standard' else 199
                if cycle_choice == 'Yearly':
                    price = 950 if plan_choice == 'Standard' else 1910
                buyer_hists.append(premium_history(
                    user=b_obj,
                    plan=plan_choice,
                    billing_cycle=cycle_choice,
                    payment_method=random.choice(PAYMENT_METHODS),
                    price=price,
                    coupon_code=random.choice(['', 'WELCOME50', 'PREMIUM100']),
                    start_date=meta['date_joined']
                ))

        verification_details.objects.bulk_create(verifs)
        bank_details.objects.bulk_create(banks)
        Cart.objects.bulk_create(carts)
        premium_buyer.objects.bulk_create(buyer_prems)
        premium_history.objects.bulk_create(buyer_hists)

        self.stdout.write(self.style.SUCCESS(f"  Created {len(created_farmer_users)} Farmers and {len(created_buyer_users)} Buyers with full profiles, banking, and limits."))

        # ─────────────────────────────────────────────────────────────────────
        # 2. CREATE CROPS
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n[2/12] Generating {num_crops_count} Crop Listings..."))

        crops_to_create = []
        for i in range(num_crops_count):
            farmer_u = random.choice(created_farmer_users)
            c_meta = random.choice(CROPS_CATALOG)
            price = random.randint(c_meta['min_p'], c_meta['max_p'])
            quantity = random.randint(300, 10000)

            crops_to_create.append(crop(
                user=farmer_u,
                cropname=c_meta['name'],
                category=c_meta['cat'],
                quantity=quantity,
                price=price,
                description=c_meta['desc'],
                is_approved=True
            ))

        created_crops = crop.objects.bulk_create(crops_to_create)
        self.stdout.write(self.style.SUCCESS(f"  Created {len(created_crops)} Crop listings."))

        # ─────────────────────────────────────────────────────────────────────
        # 3. CREATE ORDERS (NATURAL 12-MONTH HISTORICAL DISTRIBUTION)
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING(f"\n[3/12] Generating {num_orders_count} Orders across the last 12 months..."))

        orders_to_create = []
        orders_meta = []
        start_ord = Order.objects.count() + 10000

        # Create monthly weight distribution (steady month-on-month growth)
        # Month 12 ago -> 4% of total orders, Month 1 ago -> 12% of total orders
        month_weights = [4, 5, 5, 6, 7, 8, 8, 9, 10, 11, 13, 14]

        for i in range(num_orders_count):
            buyer_u = random.choice(created_buyer_users)
            status = random.choices(ORDER_STATUSES, weights=[40, 20, 15, 10, 8, 4, 3])[0]
            p_method = random.choice(PAYMENT_METHODS)
            p_status = "Paid" if status in ["Delivered", "Shipped", "Confirmed"] else random.choice(PAYMENT_STATUSES)

            # Distribute dates month by month
            m_offset = random.choices(range(12), weights=month_weights)[0]
            days_ago = (m_offset * 30) + random.randint(0, 29)
            created_at = now - timedelta(days=days_ago)

            chosen_crops = random.sample(created_crops, random.randint(1, 3))
            items_list = []
            subtotal = 0

            for c_item in chosen_crops:
                qty = random.randint(10, 250)
                sub = c_item.price * qty
                subtotal += sub
                items_list.append({
                    'crop': c_item,
                    'crop_name': c_item.cropname,
                    'price': c_item.price,
                    'quantity': qty,
                    'subtotal': sub
                })

            tax = round(subtotal * 0.05, 2)
            total_amt = subtotal + tax

            ord_id = f"#ORD-2025-{start_ord+i:05d}"
            orders_to_create.append(Order(
                user=buyer_u,
                order_id=ord_id,
                subtotal=subtotal,
                tax=tax,
                total_amount=total_amt,
                status=status,
                payment_method=p_method,
                payment_status=p_status,
                created_at=created_at
            ))
            orders_meta.append(items_list)

        created_orders = Order.objects.bulk_create(orders_to_create)

        order_items_to_create = []
        for o_obj, items_data in zip(created_orders, orders_meta):
            for itm in items_data:
                order_items_to_create.append(OrderItem(
                    order=o_obj,
                    crop=itm['crop'],
                    crop_name=itm['crop_name'],
                    price=itm['price'],
                    quantity=itm['quantity'],
                    subtotal=itm['subtotal']
                ))

        OrderItem.objects.bulk_create(order_items_to_create)
        self.stdout.write(self.style.SUCCESS(f"  Created {len(created_orders)} Orders and {len(order_items_to_create)} Order Items."))

        # ─────────────────────────────────────────────────────────────────────
        # 4. CREATE FARMER TOOLS & MACHINERY
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n[4/12] Generating Farmer Tools & Heavy Machinery..."))

        tools_to_create = []
        for i in range(120):
            farmer_u = random.choice(created_farmer_users)
            t_meta = random.choice(TOOL_CATALOG)

            tools_to_create.append(FarmerTool(
                user=farmer_u,
                tool_name=f"{t_meta['name']} #{i+1}",
                category=t_meta['cat'],
                company=t_meta['company'],
                model_name=t_meta['model'],
                manufacturing_year=random.randint(2018, 2025),
                horsepower=t_meta['hp'],
                condition=random.choice(['excellent', 'good', 'average']),
                description=f"Well maintained {t_meta['name']} ready for field operation in Saurashtra.",
                availability_status='available',
                location=f"{farmer_u.city}, Gujarat",
                original_price=t_meta['orig'],
                predicted_price=t_meta['pred'],
                years_used=random.randint(1, 6)
            ))

        FarmerTool.objects.bulk_create(tools_to_create)
        self.stdout.write(self.style.SUCCESS("  Created Farmer Tools & Machinery listings."))

        # ─────────────────────────────────────────────────────────────────────
        # 5. CREATE BLOGS & NEWS ARTICLES
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n[5/12] Generating Blogs & News Articles..."))

        # Bloag model title has max_length=20 and unique=True!
        blog_titles = [
            "Organic Wheat Tips", "Cotton Pest Control", "Jeera Export Guide",
            "Smart Drip System", "Groundnut Oil Rate", "Solar Pump Subsidy",
            "Soybean Crop Care", "Onion Storage Ideas", "Mustard Seed Variety",
            "Soil Health Cards", "Modern Agri Tools", "Kisan Credit Scheme",
            "Drip Irrigation 26", "Weather Crop Alerts", "Saurashtra Farming",
            "Unjha Market Trends", "Organic Fertilizer", "Natural Pesticides",
            "Rain Harvest Tech", "Agri Market 2026"
        ]

        blogs_to_create = []
        for idx, title in enumerate(blog_titles):
            author = random.choice(created_farmer_users)
            blogs_to_create.append(bloag(
                user=author,
                title=title,
                content=(
                    f"Comprehensive article discussing {title}. Organic farming and modern agriculture techniques "
                    "help Indian farmers increase crop yield while protecting soil health and reducing input costs. "
                    "Using scientific crop rotation and natural fertilizers produces premium quality produce."
                )
            ))

        bloag.objects.bulk_create(blogs_to_create, ignore_conflicts=True)

        news_titles = [
            ("Central Govt Announces New Subsidies for Drip Irrigation", "Government Updates"),
            ("Unjha Mandi Sees Record Cumin (Jeera) Export Demand", "Market Prices"),
            ("Monsoon Forecast 2026: Normal Rainfall Expected Across Gujarat", "Weather Alerts"),
            ("High Yield Hybrid Cotton Varieties Approved for Saurashtra", "Crop News"),
            ("AI-Driven Crop Price Prediction Tool Launched for Farmers", "Technology"),
            ("Organic Fertilizer Subsidy Scheme Expanded nationwide", "Government Updates"),
            ("Dairy Farmers Receive Extra Bonus on Milk Procurement Rates", "Dairy Farming")
        ]

        news_to_create = []
        for i in range(50):
            t_pair = random.choice(news_titles)
            news_to_create.append(news(
                title=f"{t_pair[0]} #{i+1}",
                description="Detailed news coverage regarding recent agricultural developments, government policy updates, and market trends.",
                category=t_pair[1],
                state=random.choice(["Central Government", "Gujarat", "Maharashtra", "Rajasthan"]),
                is_breaking=random.choice([True, False, False]),
                breaking_hours=24
            ))

        news.objects.bulk_create(news_to_create)
        self.stdout.write(self.style.SUCCESS("  Created Agriculture Blogs and News articles."))

        # ─────────────────────────────────────────────────────────────────────
        # 6. CREATE GOVERNMENT SCHEMES (GOV_INFO)
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n[6/12] Generating Government Schemes (Gov Info)..."))

        gov_schemes = [
            ("PM-KISAN Samman Nidhi Yojana", "Financial benefit of Rs 6000 per year for eligible farmer families."),
            ("Pradhan Mantri Fasal Bima Yojana (PMFBY)", "Comprehensive crop insurance coverage against natural calamities."),
            ("Kisan Credit Card (KCC) Scheme", "Concessional credit access to farmers for agricultural inputs."),
            ("Solar Powered Agriculture Pump Scheme", "Up to 80% subsidy for installing solar water pumps."),
            ("Gujarat Krishi Sahay Yojana", "State disaster financial relief for crop damages due to rain or drought."),
            ("Sub-Mission on Agricultural Mechanization", "Subsidies for buying tractors, harvesters, and rotavators.")
        ]

        gov_to_create = []
        for i, (stitle, sdesc) in enumerate(gov_schemes):
            gov_to_create.append(gov_info(
                title=stitle,
                description=sdesc,
                oneline_info=sdesc[:200],
                state=random.choice(["Central Government", "Gujarat", "Maharashtra"]),
                source_link="https://agricoop.gov.in",
                department="Ministry of Agriculture & Farmers Welfare"
            ))

        gov_info.objects.bulk_create(gov_to_create)
        self.stdout.write(self.style.SUCCESS("  Created Government Schemes data."))

        # ─────────────────────────────────────────────────────────────────────
        # 7. CREATE COMMUNITY POSTS
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n[7/12] Generating Community Messages & Discussions..."))

        community_to_create = []
        for i in range(250):
            sender = random.choice(created_farmer_users)
            topic = random.choice(COMMUNITY_TOPICS)
            community_to_create.append(community_message(
                sender=sender,
                message=topic
            ))

        community_message.objects.bulk_create(community_to_create)
        self.stdout.write(self.style.SUCCESS("  Created Community Posts."))

        # ─────────────────────────────────────────────────────────────────────
        # 8. CREATE AI CHATBOT ROOMS & CONVERSATIONS
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n[8/12] Generating AI Chatbot Conversations..."))

        chat_rooms_to_create = []
        for i in range(60):
            u_obj = random.choice(created_farmer_users + created_buyer_users)
            chat_rooms_to_create.append(chatroom(user=u_obj))

        created_chat_rooms = chatroom.objects.bulk_create(chat_rooms_to_create)

        messages_to_create = []
        for room in created_chat_rooms:
            for role, content in AI_CONVERSATIONS:
                messages_to_create.append(message(
                    chat_room=room,
                    role=role,
                    content=content
                ))

        message.objects.bulk_create(messages_to_create)
        self.stdout.write(self.style.SUCCESS("  Created AI Chatbot rooms and conversation history."))

        # ─────────────────────────────────────────────────────────────────────
        # 9. CREATE WISHLIST (SAVED CROPS) & CART ITEMS
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n[9/12] Generating Wishlist and Cart Items..."))

        saved_to_create = []
        for i in range(1500):
            b_obj = random.choice(created_buyers)
            c_obj = random.choice(created_crops)
            saved_to_create.append(saved(user=b_obj, crop=c_obj))

        saved.objects.bulk_create(saved_to_create, ignore_conflicts=True)

        cart_items_to_create = []
        all_carts = Cart.objects.all()
        for c_obj in random.sample(list(all_carts), min(100, len(all_carts))):
            crop_pick = random.choice(created_crops)
            cart_items_to_create.append(CartItem(
                cart=c_obj,
                crop=crop_pick,
                quantity=random.randint(50, 300)
            ))

        CartItem.objects.bulk_create(cart_items_to_create, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS("  Created Wishlist items and active Carts."))

        # ─────────────────────────────────────────────────────────────────────
        # 10. CREATE NOTIFICATIONS
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n[10/12] Generating Notifications..."))

        notif_templates = [
            ("Order", "Your order #{ord} for {crop} has been confirmed."),
            ("Order", "Order #{ord} has been shipped via express transport."),
            ("Payment", "Payment of ₹{amt} received successfully."),
            ("Premium", "Your Premium Plan subscription is active now! Enjoy full benefits."),
            ("Bulk", "New bulk procurement request matched your listed crops."),
            ("Export", "Export inquiry for {crop} approved by sub-admin.")
        ]

        notifs_to_create = []
        for i in range(3000):
            b_obj = random.choice(created_buyers)
            ntype, template = random.choice(notif_templates)
            msg = template.format(
                ord=random.randint(1000, 9999),
                crop=random.choice(CROPS_CATALOG)['name'],
                amt=random.randint(1500, 45000)
            )
            notifs_to_create.append(notifications(
                user=b_obj,
                notification_type=ntype,
                message=msg[:100],
                is_readed=random.choice([True, False])
            ))

        notifications.objects.bulk_create(notifs_to_create)
        self.stdout.write(self.style.SUCCESS("  Created Notifications."))

        # ─────────────────────────────────────────────────────────────────────
        # 11. CREATE EXPORT INQUIRIES
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n[11/12] Generating Export Inquiries..."))

        exports_to_create = []
        for i in range(250):
            b_obj = random.choice(created_buyers)
            c_meta = random.choice(CROPS_CATALOG)

            exports_to_create.append(exportinquiry(
                user=b_obj,
                country=random.choice(EXPORT_COUNTRIES),
                crop_name=c_meta['name'],
                required_quantity=random.randint(5000, 60000),
                packaging_type=random.choice(PACKAGING_TYPES),
                quality_standard=random.choice(QUALITY_STANDARDS),
                shipping_port=random.choice(PORTS),
                expected_price=random.randint(c_meta['min_p'], c_meta['max_p']),
                expected_delivery=(now + timedelta(days=random.randint(15, 90))).date(),
                additional_notes="Phytosanitary inspection certificate required upon loading."
            ))

        exportinquiry.objects.bulk_create(exports_to_create)
        self.stdout.write(self.style.SUCCESS("  Created Export Inquiries."))

        # ─────────────────────────────────────────────────────────────────────
        # 12. CREATE BULK PROCUREMENT REQUESTS
        # ─────────────────────────────────────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("\n[12/12] Generating Bulk Procurement Requests..."))

        bulks_to_create = []
        for i in range(250):
            b_obj = random.choice(created_buyers)
            c_meta = random.choice(CROPS_CATALOG)

            bulks_to_create.append(bulkrequest(
                user=b_obj,
                crop_name=c_meta['name'],
                category=c_meta['cat'],
                required_quantity=random.randint(2000, 40000),
                unit='kg',
                target_price=random.randint(c_meta['min_p'], c_meta['max_p']),
                required_date=(now + timedelta(days=random.randint(10, 60))).date(),
                delivery_state=random.choice(STATES),
                delivery_district=random.choice(GUJARAT_CITIES),
                additional_notes="Direct farm procurement contract.",
                status=random.choice(['Draft', 'Pending', 'Approved', 'Completed'])
            ))

        bulkrequest.objects.bulk_create(bulks_to_create)
        self.stdout.write(self.style.SUCCESS("  Created Bulk Procurement Requests."))

        self.stdout.write(self.style.SUCCESS("\nDATABASE SEEDING COMPLETED SUCCESSFULLY!"))
        self.stdout.write(self.style.SUCCESS(
            f"Summary: {num_farmers} Farmers, {num_buyers} Buyers, {num_crops_count} Crops, "
            f"{num_orders_count} Orders (12-Month Distribution), {len(tools_to_create)} Tools, "
            f"{len(blogs_to_create)} Blogs, {len(news_to_create)} News, {len(gov_to_create)} Gov Schemes, "
            f"{len(community_to_create)} Community Messages, {len(created_chat_rooms)} AI Chatbot Rooms, "
            f"plus Wishlists, Carts, Export & Bulk Inquiries fully populated."
        ))
