from django.shortcuts import render

# Create your views here.
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')

def admin_inventory(request):
    items = Inventory.objects.all()
    return render(request, 'admin/inventory.html', {'items': items})
