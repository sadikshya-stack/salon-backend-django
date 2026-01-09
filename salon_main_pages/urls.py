from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('gallery/', views.gallery, name='gallery'),
    path('appointments/', views.appointments, name='appointments'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.products, name='products'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/appointments/', views.admin_appointments, name='admin_appointments'),
    path('admin/services/', views.admin_services, name='admin_services'),
    path('admin/inventory/', views.admin_inventory, name='admin_inventory'),
    path('admin/staff/', views.admin_staff, name='admin_staff'),
    path('admin/customers/', views.admin_customers, name='admin_customers'),
    path('admin/reports/', views.admin_reports, name='admin_reports'),
    path('admin/settings/', views.admin_settings, name='admin_settings'),
    path('admin/profile/', views.admin_profile, name='admin_profile'),
]


