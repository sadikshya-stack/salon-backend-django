from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import Appointment

class GlamourAdminSite(AdminSite):
    site_header = "Glamour Touch Admin"
    site_title = "Glamour Touch"
    index_title = "Dashboard"

    def admin_dashboard(self, request):
        # Get upcoming appointments for dashboard
        today = timezone.now().date()
        upcoming_appointments = Appointment.objects.filter(
            appointment_date__gte=today,
            appointment_date__lte=today + timedelta(days=7),
            status='scheduled'
        ).select_related('customer', 'service', 'staff__user').order_by('appointment_date', 'appointment_time')
        
        # Create dummy appointments if none exist
        if not upcoming_appointments:
            from .models import User, Service, Staff
            if User.objects.exists() and Service.objects.exists() and Staff.objects.exists():
                # Create sample data for display
                sample_appointments = [
                    {
                        'client_name': 'John Doe',
                        'service_name': 'Haircut',
                        'date': '2024-01-15',
                        'status': 'scheduled'
                    },
                    {
                        'client_name': 'Jane Smith',
                        'service_name': 'Hair Coloring',
                        'date': '2024-01-16',
                        'status': 'scheduled'
                    },
                    {
                        'client_name': 'Mike Johnson',
                        'service_name': 'Beard Trim',
                        'date': '2024-01-17',
                        'status': 'scheduled'
                    }
                ]
                context = {
                    'appointments': sample_appointments
                }
            else:
                context = {'appointments': []}
        else:
            # Convert real appointments to the format expected by template
            appointment_list = []
            for apt in upcoming_appointments:
                appointment_list.append({
                    'client_name': f"{apt.customer.first_name} {apt.customer.last_name}",
                    'service_name': apt.service.name,
                    'date': f"{apt.appointment_date} {apt.appointment_time}",
                    'status': apt.status
                })
            context = {
                'appointments': appointment_list
            }
        
        return render(request, "admin/index.html", context)

    def get_urls(self):
        from django.urls import include
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.admin_dashboard), name='index'),
        ]
        return custom_urls + urls

# Instantiate your custom admin
glamour_admin = GlamourAdminSite(name='glamour_admin')
