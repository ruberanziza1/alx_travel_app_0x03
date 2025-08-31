from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_booking_confirmation_email(booking_id):
    """
    Send a booking confirmation email to the user.
    This is a background task that will be executed by Celery.
    """
    from .models import Booking
    
    try:
        booking = Booking.objects.get(booking_id=booking_id)
        
        # Email subject
        subject = f'Booking Confirmation - {booking.listing.title}'
        
        # Email content
        html_message = f"""
        <html>
        <body>
            <h2>Booking Confirmation</h2>
            <p>Dear {booking.user},</p>
            <p>Your booking has been confirmed successfully!</p>
            
            <h3>Booking Details:</h3>
            <ul>
                <li><strong>Property:</strong> {booking.listing.title}</li>
                <li><strong>Check-in:</strong> {booking.start_date}</li>
                <li><strong>Check-out:</strong> {booking.end_date}</li>
                <li><strong>Booking ID:</strong> {booking.booking_id}</li>
                <li><strong>Price per night:</strong> ${booking.listing.price_per_night}</li>
            </ul>
            
            <p>Thank you for choosing our service!</p>
            <p>Best regards,<br>ALX Travel App Team</p>
        </body>
        </html>
        """
        
        # Plain text version
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[booking.user],  # In a real app, you'd use actual email addresses
            html_message=html_message,
            fail_silently=False,
        )
        
        print(f"Booking confirmation email sent successfully for booking {booking_id}")
        return True
        
    except Booking.DoesNotExist:
        print(f"Booking with ID {booking_id} not found")
        return False
    except Exception as e:
        print(f"Error sending booking confirmation email: {str(e)}")
        return False 