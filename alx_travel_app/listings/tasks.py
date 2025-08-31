from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_booking_confirmation(email, booking_details):
    subject = "Booking Confirmation"
    message = f"Your booking was successful!\nDetails: {booking_details}"
    from_email = "noreply@alxtravel.com"
    send_mail(subject, message, from_email, [email])
