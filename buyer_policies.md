# 📜 KRUSHI MITRA (कृषि मित्र) — COMPREHENSIVE BUYER POLICIES & TERMS

---

## 📌 TABLE OF CONTENTS
1. [Buyer Verification & KYC Policy](#1-buyer-verification--kyc-policy)
2. [Procurement, Pricing & Payment Policy](#2-procurement-pricing--payment-policy)
3. [Order Cancellation, Return & Refund Policy](#3-order-cancellation-return--refund-policy)
4. [Quality Inspection & Grading Dispute Policy](#4-quality-inspection--grading-dispute-policy)
5. [Bulk Procurement & Export Inquiry Policy](#5-bulk-procurement--export-inquiry-policy)
6. [Logistics, Shipping & Delivery Policy](#6-logistics-shipping--delivery-policy)
7. [Buyer Subscription & Premium Membership Policy](#7-buyer-subscription--premium-membership-policy)
8. [Buyer Code of Conduct & Fraud Prevention Policy](#8-buyer-code-of-conduct--fraud-prevention-policy)

---

## 🔐 1. BUYER VERIFICATION & KYC POLICY

### 1.1 Mandatory Verification Requirement
To maintain marketplace trust and facilitate legal agricultural transactions between farmers and buyers, all registered buyers on Krushi Mitra must complete mandatory Know-Your-Customer (KYC) verification before placing orders exceeding ₹10,000 or initiating bulk/export requests.

### 1.2 Required Verification Documents
Buyers must upload authentic copies of the following documents under `buyer_verification` & `buyer_bank_details`:
* **Business Identification**:
  * Valid **GST Registration Certificate** (GSTIN).
  * **Trade License** / APMC Trader License (Mandatory for commission agents and wholesale traders).
  * **MSME / Udyam Registration Certificate** (Optional for small enterprises).
* **Identity & Address Proof**:
  * Government-issued **Aadhaar Card** (Front & Back).
  * Business Owner / Authorized Representative **PAN Card**.
* **Financial & Bank Settlement Details**:
  * Cancelled Cheque or Bank Passbook copy showing Account Name, Account Number, and IFSC Code.

### 1.3 Approval Timeline & SLA
* **Verification Window**: Sub-admins review submitted KYC applications within **24 to 48 business hours**.
* **Account Status**:
  * `Verified`: Full access to browse crops, place cart orders, submit bulk requests, and contact farmers directly.
  * `Pending`: Limited browsing; ordering restricted.
  * `Rejected / Action Required`: Buyer will receive a notification outlining missing or illegible documents. Resubmission must occur within 7 days.

---

## 💳 2. PROCUREMENT, PRICING & PAYMENT POLICY

### 2.1 Pricing Transparency
* All crop prices listed on Krushi Mitra are expressed in **Rupees per Quintal (100 KG)** or **Rupees per Kilogram (KG)**.
* Prices listed by farmers do not include applicable local government taxes, APMC mandi fees, or shipping/transportation charges unless explicitly stated.

### 2.2 Applicable Taxes & Platform Fees
* **GST & Agricultural Taxes**: Standard taxes (default 5% or applicable statutory rate) are automatically added to the cart subtotal (`Cart.tax_per`).
* **Platform Fee**: Standard buyers pay a nominal transaction processing fee. **Premium Plan** buyers enjoy 0% platform transaction fees.

### 2.3 Escrow Payment Mechanism
To protect buyers against non-delivery and farmers against non-payment:
1. **Payment Deposit**: Upon order confirmation, the full payment amount is deposited into Krushi Mitra Escrow Account via UPI, NetBanking, NEFT/RTGS, or Debit/Credit Card.
2. **Fund Hold**: Escrow holds funds securely until the buyer inspects and approves the delivery at the destination warehouse.
3. **Seller Settlement**: Funds are released to the farmer’s KYC-verified bank account within **24 to 48 hours** following physical delivery confirmation.

### 2.4 Coupon & Discount Policy
* **Discount Coupons (`discount_coupon`)**: Valid on eligible crop cart orders meeting minimum order thresholds (`minimum_amount`).
* Coupons are single-use per buyer unless specified otherwise and cannot be redeemed for physical cash.

---

## 🔄 3. ORDER CANCELLATION, RETURN & REFUND POLICY

### 3.1 Order Cancellation Rules
* **Before Dispatch (100% Refund)**: Buyers may cancel an order free of charge at any time prior to the seller dispatching the shipment (`status = 'Pending'`).
* **After Dispatch**: Orders cannot be cancelled once logistics transit has commenced (`status = 'Shipped'`), except in cases of major delivery delay (>72 hours past scheduled SLA) or seller default.

### 3.2 Quality Discrepancy & Return Eligibility
Crops are perishable commodities; therefore, returns are strictly governed by unloading inspection standards:
* **Eligible Return Reasons**:
  1. **Grade Mismatch**: Received crop grade significantly differs from listed photos/specs (e.g., received Grade C instead of ordered Grade A).
  2. **Severe Damage / Rotting**: Moisture content exceeding agreed limits resulting in rotting during transit (>10% damaged goods).
  3. **Quantity Shortfall**: Delivered weight falls short by $>3\%$ of the ordered quintals (seller must adjust billing or complete delivery).
* **Ineligible Return Reasons**:
  * Change of mind after unloading.
  * Minor natural variation in crop size/color consistent with agricultural standards.
  * Damage caused by buyer's delayed unloading at destination (>6 hours waiting time).

### 3.3 Refund Process & SLA
* **Claim Window**: Quality or quantity disputes must be raised on the Buyer Panel within **12 hours of delivery arrival**.
* **Refund SLA**: Approved refunds are credited back to the buyer's original payment method / registered bank account within **3 to 5 business days**.

---

## 🔬 4. QUALITY INSPECTION & GRADING DISPUTE POLICY

### 4.1 On-Arrival Quality Inspection
* Buyers have the right to inspect the cargo at the time of truck arrival before signing the Proof of Delivery (POD).
* For bulk orders ($>100\text{ Quintals}$), moisture testing and random bag sampling (up to 5% of total bags) are permitted.

### 4.2 Dispute Resolution Framework
In case of quality disagreement between farmer and buyer:
1. **Third-Party APMC Quality Inspection**: A certified APMC quality inspector or Krushi Mitra field officer will perform an on-site sample analysis.
2. **Price Re-Negotiation**: If quality is slightly below grade but acceptable, Krushi Mitra facilitates an mutually agreed price deduction.
3. **Full Cargo Rejection**: If quality fails statutory safety or pesticide residue limits, full cargo rejection is approved, and 100% escrow refund is triggered for the buyer.

---

## 📦 5. BULK PROCUREMENT & EXPORT INQUIRY POLICY

### 5.1 Bulk Procurement Requests (`bulkrequest`)
* **Eligibility**: Available to Verified and Premium buyers.
* **Minimum Order Threshold**: Minimum 50 Quintals (5,000 KG) per bulk request.
* **Process**:
  * Buyer specifies target price, required date, and delivery district/state.
  * Sub-admins and verified farmers submit competitive bids.
  * Once accepted, buyer deposits a mandatory **20% advance commitment fee** into escrow.

### 5.2 Export Inquiries (`exportinquiry`)
* **Export Requirements**: Buyers submitting export inquiries must provide:
  * Destination Country & Shipping Port.
  * Phytosanitary and quality standards (e.g., ISO, FSSAI, Organic Certification).
  * Required export packaging (e.g., 50KG Jute Bags, Vacuum Packed, Bulk Containers).
* **Custom Compliance**: Exporters are responsible for international customs clearance unless contracting Krushi Mitra’s end-to-end export logistics partner.

---

## 🚛 6. LOGISTICS, SHIPPING & DELIVERY POLICY

### 6.1 Logistics Models
* **Option A: Krushi Mitra Logistics (Recommended)**: Transport organized by Krushi Mitra logistics network. Includes full transit insurance and real-time GPS tracking.
* **Option B: Buyer Self-Pickup**: Buyer dispatches their own commercial vehicle to the farmer’s location/warehouse.

### 6.2 Demurrage & Unloading SLA
* **Free Unloading Time**: Buyers receive **4 hours of free unloading time** upon truck arrival at the designated warehouse.
* **Demurrage Charges**: Waiting time exceeding 4 hours incurs demurrage charges of ₹500 per hour payable by the buyer to the transport provider.

---

## 👑 7. BUYER SUBSCRIPTION & PREMIUM MEMBERSHIP POLICY

### 7.1 Subscription Tiers
Buyers can subscribe to Krushi Mitra Premium Plans (`premium_plans`):
* **Free Tier**: Basic crop browsing, maximum cart limit of 1,000 KG, standard customer support.
* **Standard Tier (Monthly/Yearly)**: Unlimited cart limits, access to APMC market price trends, priority customer support.
* **Premium Tier (Monthly/Yearly)**: Unlimited bulk sourcing, direct contact details for top verified farmers, 0% platform processing fee, priority export assistance.

### 7.2 Billing & Auto-Renewal
* Subscriptions can be paid monthly or annually (with yearly discount options up to 20%).
* Subscriptions automatically revert to `Free` upon expiration unless renewed before `end_date`.
* **Refundability**: Subscription plan fees are non-refundable once activated.

---

## 🛡️ 8. BUYER CODE OF CONDUCT & FRAUD PREVENTION POLICY

### 8.1 Prohibited Practices
Buyers on Krushi Mitra must refrain from the following unlawful activities:
1. **Fake Bidding & Price Manipulation**: Submitting non-genuine bulk requests to artificially depress or inflate market prices.
2. **Off-Platform Payment Collusion**: Attempting to bypass Krushi Mitra escrow to evade verification while using platform infrastructure.
3. **Harassment of Farmers**: Misbehavior or abusive communication toward farmers or Krushi Mitra field representatives.
4. **Fraudulent Document Submission**: Submitting forged GST, PAN, or bank documents.

### 8.2 Penalties & Account Suspension
* **First Offense**: Formal warning and temporary 7-day account freeze.
* **Second Offense**: Forfeiture of active subscription and permanent blacklist of GSTIN/PAN across Krushi Mitra ecosystem.

---

## 📞 9. HELP & POLICY INQUIRIES

For questions regarding these buyer policies or to initiate a dispute:
* **Buyer Voice Helpline**: Available 24/7 inside the Krushi Mitra Buyer Panel
* **Support Email**: `buyer-support@krushimitra.com`
* **Live Desk Hours**: Monday to Saturday, 8:00 AM – 7:00 PM IST
