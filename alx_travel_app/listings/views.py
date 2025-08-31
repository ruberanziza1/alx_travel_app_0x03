from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from .tasks import send_booking_confirmation

def perform_create(self, serializer):
    booking = serializer.save()
    send_booking_confirmation.delay(booking.user.email, str(booking))


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all().order_by('-created_at')
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all().order_by('-booked_at')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
