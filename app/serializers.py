from rest_framework import serializers
from .models import Accommodation

class SimpleAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = ['name',] 

class DetailedAccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        exclude = ['id',] 
