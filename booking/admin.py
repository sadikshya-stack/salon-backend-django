from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Service, ServiceType, Staff, Appointment, AvailableSlot, Contact, PaymentMethod
from django.utils.html import format_html


# ---------- User Admin ----------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Role & Permissions', {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Important Dates', {
            'fields': ('last_login',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'role',
                'password1',
                'password2',
                'is_active',
                'is_staff',
            ),
        }),
    )

    readonly_fields = ('last_login',)



# ---------- Service Admin ----------
class ServiceTypeInline(admin.TabularInline):
    model = ServiceType
    extra = 1
    fields = ('name', 'price', 'duration_minutes', 'is_active')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at', 'image_preview')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_editable = ('is_active',)

    inlines = [ServiceTypeInline]

    fieldsets = (
            ("Service Information", {
                "fields": ('name', 'description', 'is_active', 'image', 'image_preview')
            }),
            ("Timestamps", {
                "fields": ('created_at', 'updated_at'),
                "classes": ('collapse',),
            }),
        )

    readonly_fields = ('created_at', 'updated_at', 'image_preview')

    def image_preview(self, obj):
            if obj.image:
                return format_html(
                    '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:8px;" />',
                    obj.image.url
                )
            return "No Image"

    image_preview.short_description = "Preview"


# ---------- Staff Admin ----------
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'specialization', 'is_available')
    list_filter = ('is_available', 'specialization')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')

    def user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}" if obj.user else "No User"
    user_name.short_description = 'Staff'


# ---------- Appointment Admin ----------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'customer_email',
        'appointment_date',
        'appointment_time',
        'status',
        'payment_status',
        'created_at',
    )

    list_filter = (
        'status',
        'payment_status',
        'appointment_date',
    )

    search_fields = (
        'name',
        'email',
        'phone',
    )

    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Customer Info', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Appointment', {
            'fields': ('appointment_date', 'appointment_time')
        }),
        ('Payment & Status', {
            'fields': ('payment_method', 'payment_status', 'status')
        }),
        ('System', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # -------- Custom columns --------
    def customer_name(self, obj):
        return obj.name
    customer_name.short_description = "Customer"

    def customer_email(self, obj):
        return obj.email
    customer_email.short_description = "Email"



# ---------- AvailableSlot Admin ----------
@admin.register(AvailableSlot)
class AvailableSlotAdmin(admin.ModelAdmin):
    list_display = ('staff_name', 'date', 'start_time', 'end_time', 'is_available')
    list_filter = ('is_available', 'date')
    search_fields = ('staff__user__first_name', 'staff__user__last_name')

    def staff_name(self, obj):
        if obj.staff and obj.staff.user:
            return f"{obj.staff.user.first_name} {obj.staff.user.last_name}"
        return "No Staff"
    staff_name.short_description = 'Staff'



admin.site.register(Contact)
admin.site.register(ServiceType)
admin.site.register(PaymentMethod)