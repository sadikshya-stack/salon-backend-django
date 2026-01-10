from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings

from .models import AvailableSlot, Appointment, Staff


def process_appointment_slot(appointment):
    """
    Checks appointment conflicts, confirms slot if available,
    updates appointment status, and sends email.
    """

    # ---------------------------
    # FIND AVAILABLE STAFF ✅
    # ---------------------------
    available_staff = Staff.objects.filter(
        is_active=True,
        is_available=True
    )

    if not available_staff.exists():
        appointment.status = 'cancelled'
        appointment.cancelled_reason = "No staff available"
        appointment.cancelled_at = datetime.now()
        appointment.save()
        return False
    # ---------------------------
    # APPOINTMENT TIME RANGE
    # ---------------------------
    appointment_datetime = datetime.combine(
        appointment.appointment_date,
        appointment.appointment_time
    )

    # Assume service duration = 60 minutes
    appointment_end = appointment_datetime + timedelta(minutes=60)

    # ---------------------------
    # CHECK EXISTING APPOINTMENTS ❌
    # ---------------------------
    conflict_exists = Appointment.objects.filter(
        appointment_date=appointment.appointment_date,
        appointment_time=appointment.appointment_time,
        status__in=['pending', 'confirmed']
    ).exclude(id=appointment.id).exists()

    if conflict_exists:
        appointment.status = 'cancelled'
        appointment.cancelled_reason = "Time slot already booked"
        appointment.cancelled_at = datetime.now()
        appointment.save()

        send_mail(
            subject="Appointment Not Available – Glamour Touch",
            message=(
                f"Dear {appointment.name},\n\n"
                f"The appointment slot you selected has already been booked.\n\n"
                f"📅 Date: {appointment.appointment_date}\n"
                f"⏰ Time: {appointment.appointment_time}\n\n"
                f"Please choose another available time slot.\n\n"
                f"Thank you for your understanding.\n"
                f"Glamour Touch"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.email],
            fail_silently=False,
        )

        return False

    # ---------------------------
    # FIND AVAILABLE SLOT ✅
    # ---------------------------
    slot = AvailableSlot.objects.filter(
        date=appointment.appointment_date,
        start_time__lte=appointment.appointment_time,
        end_time__gte=appointment_end.time(),
        is_available=True
    ).first()

    if not slot:
        appointment.status = 'cancelled'
        appointment.cancelled_reason = "No staff available for selected time"
        appointment.cancelled_at = datetime.now()
        appointment.save()

        send_mail(
            subject="Appointment Not Available – Glamour Touch",
            message=(
                f"Dear {appointment.name},\n\n"
                f"Unfortunately, we do not have staff availability "
                f"for your selected time.\n\n"
                f"📅 Date: {appointment.appointment_date}\n"
                f"⏰ Time: {appointment.appointment_time}\n\n"
                f"Please book another appointment at a different time.\n\n"
                f"Glamour Touch"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.email],
            fail_silently=False,

        )

        return False

    # ---------------------------
    # CONFIRM APPOINTMENT ✅
    # ---------------------------
    appointment.status = 'confirmed'
    appointment.staff = slot.staff
    appointment.save()

    # Optional: Block slot (only if slots are per-hour)
    slot.is_available = False
    slot.save()

    send_mail(
        subject="Appointment Confirmed – Glamour Touch",
        message=(
            f"Dear {appointment.name},\n\n"
            f"Your appointment has been CONFIRMED successfully.\n\n"
            f"📅 Date: {appointment.appointment_date}\n"
            f"⏰ Time: {appointment.appointment_time}\n\n"
            f"Please arrive at the salon at least 30 minutes before "
            f"your scheduled time.\n\n"
            f"Thank you for choosing Glamour Touch.\n"
            f"We look forward to serving you!"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.email],
        fail_silently=False,
    )

    return True
