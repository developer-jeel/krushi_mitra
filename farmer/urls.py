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
# from buyer.urls import *

urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.login, name='login'),
    path('farmer_home', views.farmer_home, name='farmer_home'),
    path('farmer_crops', views.farmer_crops, name='farmer_crops'),
    path('delete_crop/<int:pk>', views.delete_crop, name='delete_crop'),
    path('edit_crop/<int:pk>', views.edit_crop, name='edit_crop'),
    
    path('farmer_tools', views.farmer_tools, name='farmer_tools'),
    path('tool_price', views.tool_price, name='tool_price'),
    path('add-tool', views.add_tool, name='add_tool'),

    path('farmer_blogs', views.farmer_blogs, name='farmer_blogs'),
    path('write_blog', views.write_blog, name='write_blog'),
    path('my_posts', views.my_posts, name='my_posts'),
    path('delete_blog', views.delete_blog, name='delete_blog'),

    path('farmer_profile', views.farmer_profile, name='farmer_profile'),

    path('farmer_chatbot', views.farmer_chatbot, name='farmer_chatbot'),
    path('clear_history', views.clear_history, name='clear_history'),

    path('gov_info', views.govt_info, name='gov_info'),
    path('news', views.farmer_news, name='news'),

    path('community_chat', views.community_chat, name='community_chat'),
    path('community_chat_delet/<int:pk>', views.community_chat_delet, name='community_chat_delet'),

    # ── Farmer Tool CRUD ──────────────────────────────────────────────────────
    path('my_tools',               views.my_tool_list,       name='my_tool_list'),
    path('tool_add',               views.tool_add,           name='tool_add'),
    path('tool_edit/<int:pk>',     views.tool_edit,          name='tool_edit'),
    path('tool_detail/<int:pk>',   views.tool_detail,        name='tool_detail'),
    path('tool_delete/<int:pk>',   views.tool_delete,        name='tool_delete'),
    path('get_tool_price/',        views.get_tool_price_api, name='get_tool_price_api'),

    # ── Farmer Premium ────────────────────────────────────────────────────────
    path('premium/',               views.farmer_premium,          name='farmer_premium'),
    path('premium_checkout/',      views.farmer_premium_checkout, name='farmer_premium_checkout'),
    path('current_plan/',          views.farmer_current_plan,     name='farmer_current_plan'),
]