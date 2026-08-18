# KRUSHI MITRA (कृषि मित्र) VOICE ASSISTANT KNOWLEDGE BASE

---

## 1. GENERAL PLATFORM OVERVIEW
- **Platform Name**: Krushi Mitra (Smart Agricultural Ecosystem)
- **Tagline**: Empowering Farmers with Smart Agriculture, Direct Market Access, and Expert Knowledge.
- **Target Audience**: Farmers, Agricultural Product Buyers, Machinery Owners, and Agri-Experts.
- **Supported Languages**: English, Hindi, and Regional Languages.
- **Operating Hours**: Voice AI Assistant is available 24/7. Live Support: Monday to Saturday, 8:00 AM to 7:00 PM IST.

---

## 2. FARMER SERVICES & CORE FEATURES

### A. Crop Listing & Direct Selling
- **Description**: Farmers can list their harvested crops directly on Krushi Mitra for buyers to purchase without middlemen.
- **How to List Crops**: Navigate to *Farmer Dashboard > My Crops > Add New Crop*. Specify crop name, quantity (in Quintals/KG), price per unit, quality grade, and upload photos.
- **Managing Crops**: Farmers can view, edit, or delete listed crops under the `farmer_crops` page.

### B. Agricultural Tools & Machinery Marketplace
- **Description**: Farmers can rent or purchase farming tools, tractors, seeders, and harvesters from other users or sub-admins.
- **Listing Tools**: Farmers can list their spare machinery under `tool_add` to generate additional income.
- **Tool Price Inquiry**: Callers can check standard rental/purchase rates for equipment using the `get_tool_price_api` feature.

### C. Mandi Rates & Crop Market Prices
- **Description**: Daily updated market prices across local Mandis (APMC markets).
- **Price Frequency**: Updated daily by 10:00 AM IST.
- **How to Query**: Callers can state their State, District, and Crop Name (e.g., "Wheat price in Rajkot today").

### D. Weather Forecasting & Crop Advisory
- **Description**: Provides 7-day hyper-local weather forecasts and advisory for rain, humidity, temperature, and wind speed.
- **Advisory Warnings**: Provides alerts for frost, heavy rainfall, or extreme heat to protect standing crops.

### E. Government Schemes & Financial Subsidies
- **Description**: Detailed information on central and state farming schemes (e.g., PM-Kisan Samman Nidhi, Crop Insurance / Fasal Bima Yojana, Drip Irrigation Subsidies).
- **Inquiry Process**: The assistant provides eligibility criteria, required documents (Aadhaar, 7/12 land extract, bank passbook), and application links.

### F. Community Chat & Farmer Blogs
- **Community Forum**: Farmers can discuss pest issues, farming techniques, and market trends in the Community Chat (`community_chat`).
- **Farmer Blogs**: Farmers and experts write blogs on organic farming, modern technology, and soil health under `farmer_blogs`.

---

## 3. ACCOUNT VERIFICATION & KYC APPROVAL

- **Why KYC is Mandatory**: To ensure buyer and seller trust, avoid fraud, and enable direct payment transfers.
- **Required Documents**:
  1. Government ID Proof (Aadhaar Card / Voter ID)
  2. Land Ownership Proof (7/12 extract / Patta) or Rental Agreement
  3. Bank Account Details (for direct payment settlement)
- **Verification Status**: Sub-admins review and approve submitted KYC within 24 to 48 hours.
- **Status Check**: Callers can ask, "What is my KYC status?" by providing their registered phone number.

---

## 4. KRUSHI MITRA PREMIUM SUBSCRIPTION

- **Free Plan**:
  - Basic crop listing (up to 3 crops)
  - Daily Mandi prices and general weather updates
  - Access to community chat
- **Premium Plan**:
  - Unlimited crop & tool listings with featured highlight badge
  - Direct priority call/connect with bulk buyers
  - Direct access to Agri-Experts for personalized crop disease diagnosis
  - Zero-commission transaction processing on marketplace sales
- **Subscription Checkout**: Farmers can upgrade under `farmer_premium` and checkout via `premium_checkout`.

---

## 5. FREQUENTLY ASKED QUESTIONS (FAQS) FOR VOICE ASSISTANT

### Q1: How do I register on Krushi Mitra?
> **Answer**: You can register on our website or mobile app by clicking 'Register', entering your full name, 10-digit mobile number, village/district, and selecting whether you are a Farmer or a Buyer.

### Q2: Is there any fee for listing my crops?
> **Answer**: Basic crop listing is completely free for all registered farmers! You can also upgrade to our Premium plan for higher buyer visibility.

### Q3: How do I get paid when a buyer purchases my crop?
> **Answer**: Once a buyer confirms an order and it is verified, payment is transferred directly into your KYC-verified bank account within 24 to 48 hours.

### Q4: How can I check if rain will affect my harvest this week?
> **Answer**: Just tell me your village or district name, and I will check the 7-day weather forecast and rain alerts for your area immediately.

### Q5: What should I do if my crop has a pest or disease?
> **Answer**: You can upload a photo of the affected plant on our AI Chatbot or Community Chat, or talk directly to our agricultural expert by booking a consultation.

---

## 6. ESCALATION & LIVE EXPERT TRANSFER RULES

The Voice Assistant must route the call to a **Live Agri-Expert or Sub-Admin** under the following rules:

1. **Severe Crop Pest Outbreak**: Callers reporting sudden, severe pest attacks or unknown crop diseases requiring urgent intervention.
2. **KYC Verification Issues**: Delayed KYC approval exceeding 3 business days.
3. **Payment & Order Discrepancies**: Payment failures or transaction disputes between buyer and farmer.
4. **Repeated Callers**: Callers who have called 3 times in 48 hours with an unresolved request.
5. **Supervisor Transfer Request**: Caller asks to speak to an administrator or human support twice.

**Transfer Phrase**:
> *"I understand this is urgent for your farm. Let me connect you directly to our Senior Agricultural Expert. Please hold the line for a moment."*

---

## 7. VOICE-PRONUNCIATION & FORMATTING GUIDELINES

- **Currency**: Read "₹500" as "500 Rupees" or "500 रुपये".
- **Units**: Read "Quintal" clearly (e.g., "2000 rupees per quintal").
- **Numbers & Phone Numbers**: Read digits clearly and spaced out (e.g., "9 8 7 6 5...").
- **Tone**: Respectful, empathetic, simple, and polite (use respectful terms like *Kisan Bhai / Farmer Friend* when appropriate).
