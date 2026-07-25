from django.urls import path
from . import views

app_name = 'subadmin'

urlpatterns = [
    # Auth
    path('',               views.login,         name='login'),
    path('logout/',        views.logout,         name='logout'),

    # Dashboard
    path('dashboard/',     views.dashboard,      name='dashboard'),

    # Farmer Management
    path('farmers/',                          views.manage_farmers,       name='manage_farmers'),
    path('farmers/<int:pk>/',                 views.farmer_detail,        name='farmer_detail'),
    path('farmers/<int:pk>/toggle/',          views.toggle_farmer,        name='toggle_farmer'),
    path('farmers/<int:pk>/delete/',          views.delete_farmer,        name='delete_farmer'),
    path('farmers/<int:pk>/reset-password/',  views.reset_farmer_password, name='reset_farmer_password'),
    path('farmers/<int:pk>/grant-doc/',       views.grant_doc_permission,  name='grant_doc_permission'),

    # Buyer Management
    path('buyers/',                    views.manage_buyers,   name='manage_buyers'),
    path('buyers/<int:pk>/',           views.buyer_detail,    name='buyer_detail'),
    path('buyers/<int:pk>/toggle/',    views.toggle_buyer,    name='toggle_buyer'),
    path('buyers/<int:pk>/delete/',    views.delete_buyer,    name='delete_buyer'),
    path('buyers/<int:pk>/verify/',    views.verify_buyer,    name='verify_buyer'),
    path('buyers/<int:pk>/grant-doc/', views.buyer_grant_doc, name='buyer_grant_doc'),

    # Crop Management
    path('crops/',                     views.manage_crops,  name='manage_crops'),
    path('crops/<int:pk>/approve/',    views.crop_approve,  name='crop_approve'),
    path('crops/<int:pk>/reject/',     views.crop_reject,   name='crop_reject'),
    path('crops/<int:pk>/delete/',     views.crop_delete,   name='crop_delete'),

    # Tool Management
    path('tools/',                     views.manage_tools,  name='manage_tools'),
    path('tools/<int:pk>/delete/',     views.tool_delete,   name='tool_delete'),

    # Blog Management
    path('blogs/',                     views.manage_blogs,  name='manage_blogs'),
    path('blogs/<int:pk>/delete/',     views.blog_delete,   name='blog_delete'),

    # Community Management
    path('community/',                 views.manage_community,  name='manage_community'),
    path('community/<int:pk>/delete/', views.community_delete,  name='community_delete'),

    # News Management
    path('news/',                            views.manage_news,          name='manage_news'),
    path('news/add/',                        views.news_add,             name='news_add'),
    path('news/<int:pk>/edit/',              views.news_edit,            name='news_edit'),
    path('news/<int:pk>/delete/',            views.news_delete,          name='news_delete'),
    path('news/<int:pk>/toggle-breaking/',   views.news_toggle_breaking, name='news_toggle_breaking'),

    # Government Schemes Management
    path('gov-schemes/',                     views.manage_gov_schemes,   name='manage_gov_schemes'),
    path('gov-schemes/add/',                 views.gov_scheme_add,       name='gov_scheme_add'),
    path('gov-schemes/<int:pk>/edit/',        views.gov_scheme_edit,      name='gov_scheme_edit'),
    path('gov-schemes/<int:pk>/delete/',      views.gov_scheme_delete,    name='gov_scheme_delete'),

    # Order Management
    path('orders/',                          views.manage_orders,        name='manage_orders'),
    path('orders/<int:pk>/',                 views.order_detail,         name='order_detail'),
    path('orders/<int:pk>/update-status/',   views.order_update_status,  name='order_update_status'),

    # KYC & Product Approval
    path('kyc/',                             views.kyc_approval,      name='kyc_approval'),
    path('kyc/<int:pk>/grant-doc/',          views.kyc_grant_doc,     name='kyc_grant_doc'),
    path('kyc/<int:pk>/toggle-status/',       views.kyc_toggle_status, name='kyc_toggle_status'),
    path('product-approval/',                views.product_approval, name='product_approval'),

    # Premium Management
    path('premium/',                         views.manage_premium,   name='manage_premium'),
    path('premium/settings/',                views.premium_settings, name='premium_settings'),

    # Reports & Exports
    path('reports/',                         views.reports,              name='reports'),
    path('reports/export/farmers/',          views.export_farmers_csv,   name='export_farmers'),
    path('reports/export/buyers/',           views.export_buyers_csv,    name='export_buyers'),
    path('reports/export/orders/',           views.export_orders_csv,    name='export_orders'),

    # Profile & Settings
    path('profile/',                         views.profile,          name='profile'),
    path('support/',                         views.support_tickets,  name='support_tickets'),
    path('settings/',                        views.system_settings,  name='system_settings'),

    # Premium Coupon Management
    path('coupons/premium/',                         views.manage_premium_coupons,     name='manage_premium_coupons'),
    path('coupons/premium/add/',                     views.premium_coupon_add,          name='premium_coupon_add'),
    path('coupons/premium/<int:pk>/edit/',            views.premium_coupon_edit,         name='premium_coupon_edit'),
    path('coupons/premium/<int:pk>/delete/',          views.premium_coupon_delete,       name='premium_coupon_delete'),
    path('coupons/premium/<int:pk>/toggle/',          views.premium_coupon_toggle,       name='premium_coupon_toggle'),
    path('coupons/premium/<int:pk>/duplicate/',       views.premium_coupon_duplicate,    name='premium_coupon_duplicate'),

    # Discount Coupon Management
    path('coupons/discount/',                        views.manage_discount_coupons,     name='manage_discount_coupons'),
    path('coupons/discount/add/',                    views.discount_coupon_add,         name='discount_coupon_add'),
    path('coupons/discount/<int:pk>/edit/',           views.discount_coupon_edit,        name='discount_coupon_edit'),
    path('coupons/discount/<int:pk>/delete/',         views.discount_coupon_delete,      name='discount_coupon_delete'),
    path('coupons/discount/<int:pk>/toggle/',         views.discount_coupon_toggle,      name='discount_coupon_toggle'),

    # Transactions / Payment History
    path('transactions/',                            views.transactions,                name='transactions'),
    path('reports/export/premium/',                  views.export_premium_csv,          name='export_premium'),
    path('reports/export/transactions/',             views.export_transactions_csv,     name='export_transactions'),

    # Premium subscription actions
    path('premium/<int:pk>/upgrade/',                views.premium_manual_upgrade,      name='premium_manual_upgrade'),
    path('premium/<int:pk>/cancel/',                 views.premium_cancel,              name='premium_cancel'),
]

