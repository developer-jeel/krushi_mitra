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
    path('buyer_bulk_order', views.buyer_bulk_order, name='buyer_bulk_order'),
    path('buyer_order_history', views.buyer_order_history, name='buyer_order_history'),
    path('buyer_profile', views.buyer_profile, name='buyer_profile'),
    path('buyer_purchase_crop', views.buyer_purchase_crop, name='buyer_purchase_crop'),
    path('kyc', views.kyc, name='kyc'),

    path('home', views.home, name='home'),
]
