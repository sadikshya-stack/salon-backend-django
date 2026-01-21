from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import admin_dashboard, admin_inventory

urlpatterns = [
    # Default admin site
    path('dashboard/', admin_dashboard, name='adminpanel-dashboard'),
    path('inventory/', admin_inventory, name='adminpanel-inventory'),


]