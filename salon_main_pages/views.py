from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
User = get_user_model()


# Home Page
def home(request):
    context = {
        "title": "Welcome to Beauty Parlour",
        "description": "Book beauty services easily and quickly",
        "services": [
            "Hair Cut",
            "Facial",
            "Makeup",
            "Massage",
        ]
    }
    return render(request, "home.html", context)


# About Page
def about(request):
    context = {
        "title": "About Us",
        "description": "We provide professional beauty services with expert staff.",
        "experience_years": 5,
        "team_size": 10,
    }
    return render(request, "about.html", context)


def gallery(request):
    return render(request, 'gallery.html')


# Services Page
def services(request):
    context = {
        "title": "Our Services",
        "services": [
            {"name": "Hair Cut", "price": 500},
            {"name": "Facial", "price": 1500},
            {"name": "Makeup", "price": 3000},
            {"name": "Massage", "price": 2000},
        ]
    }
    return render(request, "services.html", context)


# Appointments List Page
def appointments(request):
    context = {
        "title": "Appointments",
        "appointments": [
            {
                "customer": "Sita Sharma",
                "service": "Facial",
                "date": "2026-01-05",
                "time": "11:00 AM"
            },
            {
                "customer": "Rita Thapa",
                "service": "Hair Cut",
                "date": "2026-01-06",
                "time": "2:00 PM"
            },
        ]
    }
    return render(request, "appointments.html", context)


# Appointments Create Page
def appointments_create(request):
    return HttpResponse("Appointment create page working")


# Contact Page
def contact(request):
    context = {
        "title": "Contact Us",
        "address": "Kathmandu, Nepal",
        "phone": "+977-98XXXXXXXX",
        "email": "info@beautyparlour.com"
    }
    return render(request, "contact.html", context)


# Products Page
def products(request):
    context = {
        "title": "Contact Us",
        "address": "Kathmandu, Nepal",
        "phone": "+977-98XXXXXXXX",
        "email": "info@beautyparlour.com"
    }
    return render(request, "products.html", context)


# Dashboard Page
@login_required(login_url='login')
def dashboard(request):
    if request.user.role != 'customer':
        raise Http404("Page not found")

    context = {
        "title": "Dashboard",
        "total_appointments": 25,
        "total_customers": 120,
        "total_services": 8,
    }
    return render(request, "dashboard.html", context)



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.role != 'customer':
                return render(request, 'auth/login.html', {
                    'error': 'Only customers are allowed to login here.'
                })

            if not user.is_active:
                return render(request, 'auth/login.html', {
                    'error': 'Your account is inactive.'
                })

            login(request, user)
            return redirect('dashboard')  # customer dashboard

        else:
            return render(request, 'auth/login.html', {
                'error': 'Invalid email or password'
            })

    return render(request, 'auth/login.html')



# Logout Page
def logout_view(request):
    logout(request)
    return redirect('login')





def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'auth/register.html', {
                'register_error': 'Passwords do not match'
            })

        
        if User.objects.filter(email=email).exists():
            return render(request, 'auth/register.html', {
                'register_error': 'Email already exists'
            })

        
        name_parts = full_name.split()

        first_name = name_parts[0] if len(name_parts) > 0 else ''
        last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

        
        username = first_name.lower()

        
        if User.objects.filter(username=username).exists():
            username = f"{username}_{User.objects.count()}"

        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        login(request, user)
        return redirect('dashboard')

    return render(request, 'auth/register.html')


# Admin Dashboard
def admin_dashboard(request):
    context = {
        "title": "Admin Dashboard - Beauty Parlour Management System",
        "total_appointments": 24,
        "pending_approvals": 12,
        "total_services": 36,
        "total_customers": 248,
    }
    return render(request, "admin-dashboard.html", context)


# Admin Appointments
def admin_appointments(request):
    context = {
        "title": "Admin - Appointments Management",
        "appointments": [
            {
                "id": "AP20230001",
                "customer": "John Doe",
                "service": "Haircut & Styling",
                "date": "Jun 25, 2023",
                "time": "10:00 AM",
                "status": "pending"
            },
            {
                "id": "AP20230002",
                "customer": "Jane Smith",
                "service": "Facial Treatment",
                "date": "Jun 25, 2023",
                "time": "11:30 AM",
                "status": "confirmed"
            },
            {
                "id": "AP20230003",
                "customer": "Robert Johnson",
                "service": "Manicure & Pedicure",
                "date": "Jun 25, 2023",
                "time": "2:00 PM",
                "status": "completed"
            },
        ]
    }
    return render(request, "admin-appointments.html", context)


# Admin Services
def admin_services(request):
    context = {
        "title": "Admin - Services Management",
        "services": [
            {"name": "Haircut & Styling", "category": "Hair", "price": 35, "duration": "45 min"},
            {"name": "Facial Treatment", "category": "Skin Care", "price": 65, "duration": "60 min"},
            {"name": "Manicure & Pedicure", "category": "Nails", "price": 55, "duration": "75 min"},
        ]
    }
    return render(request, "admin-services.html", context)


# Admin Inventory
def admin_inventory(request):
    context = {
        "title": "Admin - Inventory Management",
        "inventory": [
            {"name": "Shampoo", "category": "Hair Care", "stock": 3, "status": "low"},
            {"name": "Nail Polish - Red", "category": "Nail Care", "stock": 2, "status": "low"},
            {"name": "Facial Mask", "category": "Skin Care", "stock": 5, "status": "medium"},
        ]
    }
    return render(request, "admin-inventory.html", context)


# Admin Staff
def admin_staff(request):
    context = {
        "title": "Admin - Staff Management",
        "staff": [
            {"name": "Sarah Johnson", "role": "Senior Stylist", "status": "active"},
            {"name": "Mike Chen", "role": "Beautician", "status": "active"},
            {"name": "Lisa Wong", "role": "Nail Technician", "status": "active"},
        ]
    }
    return render(request, "admin-staff.html", context)


# Admin Customers
def admin_customers(request):
    context = {
        "title": "Admin - Customers Management",
        "customers": [
            {"name": "John Doe", "email": "john@example.com", "phone": "+1234567890", "total_visits": 5},
            {"name": "Jane Smith", "email": "jane@example.com", "phone": "+1234567891", "total_visits": 3},
            {"name": "Robert Johnson", "email": "robert@example.com", "phone": "+1234567892", "total_visits": 8},
        ]
    }
    return render(request, "admin-customers.html", context)


# Admin Reports
def admin_reports(request):
    context = {
        "title": "Admin - Reports & Analytics",
        "monthly_revenue": 12500,
        "total_appointments": 156,
        "popular_services": ["Haircut", "Facial", "Manicure"],
    }
    return render(request, "admin-reports.html", context)


# Admin Settings
def admin_settings(request):
    context = {
        "title": "Admin - Settings",
        "business_name": "Glamour Touch Beauty Parlour",
        "business_email": "info@glamourtouch.com",
        "business_phone": "+977-98XXXXXXXX",
    }
    return render(request, "admin-settings.html", context)


# Admin Profile
def admin_profile(request):
    context = {
        "title": "Admin Profile",
        "admin_name": "Admin User",
        "admin_email": "admin@glamourtouch.com",
        "admin_role": "System Administrator",
    }
    return render(request, "admin-profile.html", context)
