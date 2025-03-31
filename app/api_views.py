from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AccommodationFilter
from .models import Accommodation, Reservation, CancelledReservation
from .serializers import SimpleAccommodationSerializer, DetailedAccommodationSerializer, ReservationSerializer, CancelledReservationSerializer

class list_accommodations(generics.ListAPIView):
    queryset = Accommodation.objects.filter(is_available="True")
    serializer_class = SimpleAccommodationSerializer
    filterset_class = AccommodationFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']


class detailed_accommodation(generics.RetrieveAPIView):
    queryset = Accommodation.objects.filter(is_available="True")
    serializer_class = DetailedAccommodationSerializer

class create_reservation(generics.CreateAPIView):
    model = Reservation
    serializer_class = ReservationSerializer

class cancel_reservation(generics.CreateAPIView):
    model = CancelledReservation
    serializer_class = CancelledReservationSerializer
        
