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
from farmer import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.login, name='login'),
    path('farmer_home', views.farmer_home, name='farmer_home'),
    path('farmer_crops', views.farmer_crops, name='farmer_crops'),
    path('farmer_tools', views.farmer_tools, name='farmer_tools'),
    path('farmer_blogs', views.farmer_blogs, name='farmer_blogs'),
    path('write_blog', views.write_blog, name='write_blog'),
    path('my_posts', views.my_posts, name='my_posts'),
    path('delete_blog', views.delete_blog, name='delete_blog'),
    path('farmer_profile', views.farmer_profile, name='farmer_profile'),
    path('farmer_chatbot', views.farmer_chatbot, name='farmer_chatbot'),
    path('clear_history', views.clear_history, name='clear_history'),
    path('tool_price', views.tool_price, name='tool_price'),
    path('add-tool', views.add_tool, name='add_tool'),
    path('community_chat', views.community_chat, name='community_chat'),
    path('gov_info', views.govt_info, name='gov_info'),
    path('news', views.news, name='news'),


    path('buyer_home', views.buyer_home, name='buyer_home'),
    path('buyer_bulk_order', views.buyer_bulk_order, name='buyer_bulk_order'),
    path('buyer_order_history', views.buyer_order_history, name='buyer_order_history'),
    path('buyer_profile', views.buyer_profile, name='buyer_profile'),
    path('buyer_purchase_crop', views.buyer_purchase_crop, name='buyer_purchase_crop'),
    path('kyc', views.kyc, name='kyc'),

    path('home', views.home, name='home'),
]
