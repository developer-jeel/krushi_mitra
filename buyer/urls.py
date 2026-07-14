"""
URL configuration for krushi_mitra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from buyer import views

urlpatterns = [
    path('buyer_home', views.buyer_home, name='buyer_home'),
    path('dashboard/', views.buyer_dashboard, name='buyer_dashboard'),

    path('browse-crops/', views.buyer_browse_crops, name='buyer_browse_crops'),
    path('crop-details/<int:pk>', views.buyer_crop_details, name='buyer_crop_details'),


    path('cart/', views.buyer_cart, name='buyer_cart'),
    path('buyer_addto_cart/', views.buyer_addto_cart, name='buyer_addto_cart'),
    path('cart_item_delete/<int:pk>', views.cart_item_delete, name='cart_item_delete'),
    path('checkout/', views.buyer_checkout, name='buyer_checkout'),


    path('orders/', views.buyer_orders, name='buyer_orders'),
    path('order-details/<int:pk>', views.buyer_order_details, name='buyer_order_details'),
    path('wishlist/', views.buyer_wishlist, name='buyer_wishlist'),
    path('add_wishlist/<int:pk>', views.add_wishlist, name='add_wishlist'),


    path('bulk-order/', views.buyer_bulk_order, name='buyer_bulk_order'),
    path('export-inquiry/', views.buyer_export_inquiry, name='buyer_export_inquiry'),
    path('messages/', views.buyer_messages, name='buyer_messages'),
    path('notifications/', views.buyer_notifications, name='buyer_notifications'),
    path('profile/', views.buyer_profile, name='buyer_profile'),
    path('verification/', views.buyer_verification, name='buyer_verification'),
    path('bank-details/', views.buyer_bank_details, name='buyer_bank_details'),
    path('request-update/', views.buyer_request_update, name='buyer_request_update'),
    path('settings/', views.buyer_settings, name='buyer_settings'),
    path('kyc', views.kyc, name='kyc'),
    
    path('premium/', views.buyer_premium, name='buyer_premium'),
    path('premium_checkout/', views.premium_checkout, name='premium_checkout'),
    path('current_plan/', views.current_plan, name='current_plan'),
]
