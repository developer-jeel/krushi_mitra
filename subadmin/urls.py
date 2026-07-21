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
    path('buyers/',                    views.manage_buyers,  name='manage_buyers'),
    path('buyers/<int:pk>/',           views.buyer_detail,   name='buyer_detail'),
    path('buyers/<int:pk>/toggle/',    views.toggle_buyer,   name='toggle_buyer'),
    path('buyers/<int:pk>/delete/',    views.delete_buyer,   name='delete_buyer'),
    path('buyers/<int:pk>/verify/',    views.verify_buyer,   name='verify_buyer'),

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

    # Order Management
    path('orders/',                          views.manage_orders,        name='manage_orders'),
    path('orders/<int:pk>/',                 views.order_detail,         name='order_detail'),
    path('orders/<int:pk>/update-status/',   views.order_update_status,  name='order_update_status'),

    # KYC & Product Approval
    path('kyc/',                             views.kyc_approval,     name='kyc_approval'),
    path('kyc/<int:pk>/grant-doc/',          views.kyc_grant_doc,    name='kyc_grant_doc'),
    path('product-approval/',                views.product_approval, name='product_approval'),

    # Premium Management
    path('premium/',                         views.manage_premium,   name='manage_premium'),

    # Reports & Exports
    path('reports/',                         views.reports,              name='reports'),
    path('reports/export/farmers/',          views.export_farmers_csv,   name='export_farmers'),
    path('reports/export/buyers/',           views.export_buyers_csv,    name='export_buyers'),
    path('reports/export/orders/',           views.export_orders_csv,    name='export_orders'),

    # Profile & Settings
    path('profile/',                         views.profile,          name='profile'),
    path('support/',                         views.support_tickets,  name='support_tickets'),
    path('settings/',                        views.system_settings,  name='system_settings'),
]
