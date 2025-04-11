from rest_framework import serializers
from .models import Accommodation, Reservation, CancelledReservation, Notification, Rating

class SimpleAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ['name',] 

class DetailedAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        exclude = ['accommodation_id',] 

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        
class CancelledReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CancelledReservation
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'\

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'