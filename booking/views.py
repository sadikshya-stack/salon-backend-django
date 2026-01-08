from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Service, Staff, Appointment


# 🔹 PUBLIC: Appointment booking page
def appointments_create(request):
    if request.method == "POST":
        Appointment.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            service=request.POST.get('service'),

            haircut_type=request.POST.get('haircutType'),
            makeup_type=request.POST.get('makeupType'),
            manicure_type=request.POST.get('manicureType'),
            pedicure_type=request.POST.get('pedicureType'),
            skincare_type=request.POST.get('skincareType'),
            nailextension_type=request.POST.get('nailextensionType'),

            appointment_date=request.POST.get('date'),
            appointment_time=request.POST.get('time'),

            notes=request.POST.get('notes'),
            payment_method=request.POST.get('payment'),
        )
        return redirect('appointments')

    return render(request, 'appointments.html')



# 🔹 PUBLIC: Appointment list page
def appointments(request):
    all_appointments = Appointment.objects.all()
    return render(request, "appointments_list.html", {
        "appointments": all_appointments
    })


# 🔹 ADMIN DASHBOARD (staff only)
@login_required
@staff_member_required
def home(request):
    context = {
        "appointments_count": Appointment.objects.count(),
        "staff_count": Staff.objects.count(),
        "services_count": Service.objects.count(),
        "title": "Dashboard",
    }
    return render(request, "admin/booking/dashboard.html", context)
