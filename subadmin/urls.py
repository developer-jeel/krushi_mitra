from django.urls import path
from . import views

app_name = 'subadmin'

urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('kyc_approval/', views.kyc_approval, name='kyc_approval'),
    path('manage_buyers/', views.manage_buyers, name='manage_buyers'),
    path('manage_farmers/', views.manage_farmers, name='manage_farmers'),
    path('order_management/', views.order_management, name='order_management'),
    path('product_approval/', views.product_approval, name='product_approval'),
    path('profile/', views.profile, name='profile'),
    path('reports/', views.reports, name='reports'),
    path('support_tickets/', views.support_tickets, name='support_tickets'),
    path('system_settings/', views.system_settings, name='system_settings'),
]
