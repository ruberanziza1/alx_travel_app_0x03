#!/usr/bin/env python
"""
Test script for Celery background tasks
Run this script to test the email notification functionality
"""

import os
import django
import uuid
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
django.setup()

from listings.models import Listing, Booking
from listings.tasks import send_booking_confirmation_email

def create_test_data():
    """Create test listing and booking for testing"""
    
    # Create a test listing
    listing = Listing.objects.create(
        title="Test Beach House",
        description="Beautiful beach house with ocean view",
        price_per_night=150.00,
        available_from=date.today(),
        available_to=date.today() + timedelta(days=30)
    )
    
    print(f"Created test listing: {listing.title} (ID: {listing.listing_id})")
    
    # Create a test booking
    booking = Booking.objects.create(
        listing=listing,
        user="test@example.com",
        start_date=date.today() + timedelta(days=7),
        end_date=date.today() + timedelta(days=10)
    )
    
    print(f"Created test booking: {booking.booking_id}")
    return booking

def test_email_task():
    """Test the email notification task"""
    
    print("=== Testing Celery Email Task ===")
    
    # Create test data
    booking = create_test_data()
    
    # Test the email task
    print(f"\nTriggering email task for booking: {booking.booking_id}")
    result = send_booking_confirmation_email.delay(str(booking.booking_id))
    
    print(f"Task submitted with ID: {result.id}")
    print("Check your Celery worker logs to see the task execution")
    
    return result

def test_task_synchronously():
    """Test the email task synchronously (for debugging)"""
    
    print("=== Testing Email Task Synchronously ===")
    
    # Create test data
    booking = create_test_data()
    
    # Test the email task synchronously
    print(f"\nRunning email task synchronously for booking: {booking.booking_id}")
    result = send_booking_confirmation_email(str(booking.booking_id))
    
    if result:
        print("✅ Email task completed successfully")
    else:
        print("❌ Email task failed")
    
    return result

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--sync":
        test_task_synchronously()
    else:
        test_email_task()
        
    print("\n=== Test Complete ===")
    print("Make sure your Celery worker is running to process the task:")
    print("celery -A alx_travel_app worker --loglevel=info") 