from django.shortcuts import render
from booking.models import InventoryItem, Service, Appointment, User
from django.shortcuts import render
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



@login_required(login_url='/login/')
def admin_dashboard(request):
    if not request.user.is_superuser:  # or request.user.role != 'admin'
       messages.error(request, "Only Admins are authorized to access this page. Login first.")
       return redirect('/login')  # redirect to some page if not admin


    today = now().date()

    context = {
        # Stats
        "today_appointments": Appointment.objects.filter(
            appointment_date=today
        ).count(),

        "pending_appointments": Appointment.objects.filter(
            status="pending"
        ).count(),

        "total_services": Service.objects.filter(
            is_active=True
        ).count(),

        "total_customers": User.objects.filter(
            role="customer",
            is_active=True
        ).count(),

        # Recent appointments (NO customer here)
        "recent_appointments": Appointment.objects.select_related(
            "staff", "payment_method"
        ).order_by("-created_at")[:5],

        # Popular services
        "popular_services": Service.objects.filter(
            is_active=True
        )[:5],

        # Low stock items
        "low_stock_items": InventoryItem.objects.filter(
            status=InventoryItem.StockStatus.LOW_STOCK
        )[:5],
    }

    return render(request, "salon_admin/dashboard.html", context)

@login_required(login_url='/login/')
def admin_inventory(request):
    if not request.user.is_superuser:  # or request.user.role != 'admin'
       messages.error(request, "Only Admins are authorized to access this page. Login first.")
       return redirect('/login')  # redirect to some page if not admin

    items = InventoryItem.objects.filter(is_active=True).select_related('category')

    context = {
        'items': items,
        'total_products': items.count(),
        'in_stock': items.filter(status=InventoryItem.StockStatus.IN_STOCK).count(),
        'low_stock': items.filter(status=InventoryItem.StockStatus.LOW_STOCK).count(),
        'out_of_stock': items.filter(status=InventoryItem.StockStatus.OUT_OF_STOCK).count(),
    }

    return render(request, 'salon_admin/inventory.html', context)

