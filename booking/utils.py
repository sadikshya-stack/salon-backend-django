from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import AvailableSlot


def process_appointment_slot(appointment):
    """
    Checks slot availability and updates appointment + sends email
    """

    appointment_datetime = datetime.combine(
        appointment.appointment_date,
        appointment.appointment_time
    )

    # Assume service duration = 60 minutes (can improve later)
    appointment_end = appointment_datetime + timedelta(minutes=60)

    # Find available slot
    slot = AvailableSlot.objects.filter(
        date=appointment.appointment_date,
        start_time__lte=appointment.appointment_time,
        end_time__gte=appointment_end.time(),
        is_available=True
    ).first()

    # ---------------------------
    # SLOT AVAILABLE ✅
    # ---------------------------
    if slot:
        appointment.status = 'confirmed'
        appointment.save()

        # Mark slot unavailable
        slot.is_available = False
        slot.save()

        send_mail(
            subject="Appointment Confirmed – Glamour Touch",
            message=(
                f"Dear {appointment.name},\n\n"
                f"Your appointment has been CONFIRMED.\n\n"
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

    # ---------------------------
    # SLOT NOT AVAILABLE ❌
    # ---------------------------
    appointment.status = 'cancelled'
    appointment.cancelled_reason = "Selected time slot not available"
    appointment.cancelled_at = datetime.now()
    appointment.save()

    send_mail(
        subject="Appointment Not Available – Glamour Touch",
        message=(
            f"Dear {appointment.name},\n\n"
            f"Unfortunately, the time slot you selected is no longer available.\n\n"
            f"📅 Date: {appointment.appointment_date}\n"
            f"⏰ Time: {appointment.appointment_time}\n\n"
            f"Please book another appointment at your preferred available time.\n\n"
            f"Thank you for your understanding.\n"
            f"Glamour Touch"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.email],
        fail_silently=False,
    )


    return False
