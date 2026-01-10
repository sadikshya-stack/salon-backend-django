from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Staff, Appointment


@receiver(post_save, sender=User)
def manage_staff_profile(sender, instance, **kwargs):
    """
    Sync Staff model with User role safely
    """

    # ROLE = STAFF
    if instance.role == 'staff':
        staff, created = Staff.objects.get_or_create(user=instance)
        if not staff.is_active:
            staff.is_active = True
            staff.is_available = True
            staff.save()

    # ROLE ≠ STAFF
    else:
        staff = Staff.objects.filter(user=instance).first()
        if not staff:
            return

        # Check if staff has appointments
        has_appointments = Appointment.objects.filter(staff=staff).exists()

        if has_appointments:
            # SOFT DISABLE
            staff.is_active = False
            staff.is_available = False
            staff.save()
        else:
            # SAFE DELETE
            staff.delete()
