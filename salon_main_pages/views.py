from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from booking.models import Appointment, Contact, Service, User,ServiceType
from datetime import datetime, time, timedelta
from booking.utils import process_appointment_slot
from django.http import Http404
from django.utils import timezone


# Home Page
def home(request):
    services = Service.objects.filter(is_active=True).prefetch_related('types')
    context = {
        "title": "Welcome to Beauty Parlour",
        "description": "Book beauty services easily and quickly",
        "services": services,
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
    services = Service.objects.filter(is_active=True).prefetch_related('types')
    context = {
        "title": "Our Services",
        "services": services,
    }
    return render(request, "services.html", context)


# Appointments
@login_required(login_url='login')
def appointments(request):
    if request.user.role != 'customer':
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login')  # or redirect('home')

    # ----------------------------
    # DATA FOR TEMPLATE (GET)
    # ----------------------------
    services = Service.objects.filter(is_active=True).prefetch_related('types')

    context = {
        'services': services,
    }

    # ----------------------------
    # HANDLE FORM SUBMISSION (POST)
    # ----------------------------
    if request.method == "POST":

        user = request.user

        # ----------------------------
        # PHONE VALIDATION
        # ----------------------------
        phone = request.POST.get('phone', '').strip()

        if not phone or not phone.isdigit() or len(phone) != 10:
            messages.error(request, "Enter a valid 10-digit phone number.")
            return redirect('appointments')

        # ----------------------------
        # SERVICE TYPE VALIDATION
        # ----------------------------
        selected_service_type_ids = []

        for service in Service.objects.filter(is_active=True):
            key = f"service_type_{service.id}"
            service_type_id = request.POST.get(key)

            if service_type_id:
                selected_service_type_ids.append(service_type_id)


        if not selected_service_type_ids:
            messages.error(request, "Please select at least one service type.")
            return redirect('appointments')


        service_types = ServiceType.objects.filter(
            id__in=selected_service_type_ids,
            is_active=True
        )

        if service_types.count() != len(selected_service_type_ids):
            messages.error(request, "Invalid service type selection.")
            return redirect('appointments')

        # ----------------------------
        # DATE & TIME VALIDATION
        # ----------------------------
        appointment_date_str = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        if not appointment_date_str or not appointment_time:
            messages.error(request, "Please select appointment date and time.")
            return redirect('appointments')

        # Convert string time → Python time object
        appointment_date = datetime.strptime(appointment_date_str, "%Y-%m-%d").date()
        hour, minute = map(int, appointment_time.split(":"))
        selected_time = time(hour, minute)

        # Allowed range
        start_time = time(9, 0)   # 09:00 AM
        end_time = time(18, 0)    # 06:00 PM

        if not (start_time <= selected_time <= end_time):
            messages.error(
                request,
                "Appointments are available only between 9:00 AM and 6:00 PM."
            )
            return redirect('appointments')

        # ----------------------------
        # TODAY TIME VALIDATION (NEW)
        # ----------------------------
        now = timezone.localtime()
        selected_datetime = timezone.make_aware(
            datetime.combine(appointment_date, selected_time)
        )

        if appointment_date == now.date():
            if selected_datetime <= now:
                messages.error(request, "Please select a future time.")
                return redirect('appointments')

            if selected_datetime < now + timedelta(hours=2):
                messages.error(
                    request,
                    "Same-day appointments must be booked at least 2 hours in advance."
                )
                return redirect('appointments')


        # ----------------------------
        # CREATE APPOINTMENT
        # ----------------------------
        appointment = Appointment.objects.create(
            name=user.get_full_name() or user.username,
            email=user.email,
            phone=phone,

            appointment_date=appointment_date,
            appointment_time=selected_time,
        )

        # link selected service type
        appointment.services.add(*service_types)

        # AUTO SLOT CHECK + EMAIL
        slot_confirmed = process_appointment_slot(appointment)

        if slot_confirmed:
            messages.success(
                request,
                "Your appointment has been booked and confirmed! "
                "Please check your email for schedule details. "
                "You can also check your appointment status and details anytime from your account. "
                "Kindly arrive 10 minutes before your appointment time."
                "Thank you for choosing us!"
            )
        else:
            messages.error(
                request,
                "The selected time slot is not available. "
                "Please check your email and book another appointment."
            )

        return redirect('appointments')

    return render(request, 'appointments.html', context)





def contact(request):
    context = {}

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        context["success"] = True

    return render(request, 'contact.html', context)



# Products Page
def products(request):
    context = {
        "title": "Contact Us",
        "address": "Kathmandu, Nepal",
        "phone": "+977-98XXXXXXXX",
        "email": "info@beautyparlour.com"
    }
    return render(request, "products.html", context)



@login_required(login_url='login')
def appointment_history(request):
    # Only customers allowed
    if request.user.role != 'customer':
        raise Http404("Page not found")

    user_email = request.user.email
    today = timezone.now().date()

    appointments = Appointment.objects.filter(
        email=user_email
    ).order_by('-appointment_date', '-appointment_time')

    context = {
        "appointments": appointments,
        "page_title": "Appointment History",
    }

    return render(request, "appointment_history.html", context)



# Dashboard Page
@login_required(login_url='login')
def dashboard(request):
    if request.user.role != 'customer' or request.user.is_superuser:
        raise Http404("Page not found")

    today = timezone.now().date()

    appointments = (
        Appointment.objects
        .filter(email=request.user.email)
        .select_related('staff')
        .prefetch_related('services', 'services__service')
    )

    upcoming_appointments = appointments.filter(
        appointment_date__gte=today,
        status__in=['pending', 'confirmed']
    )

    context = {
        "appointments": upcoming_appointments
            .order_by('appointment_date', 'appointment_time')[:5],

        "total_appointments": appointments.count(),
        "upcoming_count": upcoming_appointments.count(),
        "completed_count": appointments.filter(status='completed').count(),
        "cancelled_count": appointments.filter(status='cancelled').count(),

        # unique services booked (Haircut, Makeup, etc.)
        "services_booked": appointments.values_list(
            'services__service__id', flat=True
        ).distinct().count(),
    }

    return render(request, "dashboard.html", context)




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, "Your account is inactive.")
                return render(request, 'auth/login.html')

            # Log the user in
            login(request, user)

            # Redirect based on role
            if user.is_superuser or user.role != 'customer':
                return redirect('/adminpanel/dashboard/')
            else:
                return redirect('/dashboard/')  # customer dashboard

        else:
            messages.error(request, "Invalid email or password")
            return render(request, 'auth/login.html')

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
            role="customer",
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
