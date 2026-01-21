from django.shortcuts import render
from booking.models import InventoryItem, Service, Appointment, User
from django.shortcuts import render
from django.utils.timezone import now



def admin_dashboard(request):
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

    return render(request, "admin/dashboard.html", context)


def admin_inventory(request):
    items = InventoryItem.objects.filter(is_active=True).select_related('category')

    context = {
        'items': items,
        'total_products': items.count(),
        'in_stock': items.filter(status=InventoryItem.StockStatus.IN_STOCK).count(),
        'low_stock': items.filter(status=InventoryItem.StockStatus.LOW_STOCK).count(),
        'out_of_stock': items.filter(status=InventoryItem.StockStatus.OUT_OF_STOCK).count(),
    }

    return render(request, 'admin/inventory.html', context)

