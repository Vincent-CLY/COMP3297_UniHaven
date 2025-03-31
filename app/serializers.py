from rest_framework import serializers
from .models import Accommodation, Reservation, CancelledReservation

class SimpleAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ['name',] 

class DetailedAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        exclude = ['id',] 

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        
class CancelledReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancelledReservation
        fields = '__all__'