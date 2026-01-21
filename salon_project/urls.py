from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Default admin site
    path('admin/', admin.site.urls),
    
    # Custom dashboard (accessible at /dashboard/)
    # path('dashboard/', home, name='dashboard'),
    
    # Root URL
    path('', include('salon_main_pages.urls')),
    path('', include('booking.urls')), 
    path('adminpanel/', include('admin_panel.urls')), 
]

# Admin site customizations
admin.site.site_header = 'Salon Management System'
admin.site.site_title = 'Salon Admin'
admin.site.index_title = 'Admin Panel'

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
