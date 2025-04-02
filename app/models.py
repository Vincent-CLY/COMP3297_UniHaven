from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
import xml.etree.ElementTree as ET

# Create your models here.
# Define classes, each class has its properties, specify their attribute
#  !!! Relate to the UML Graph
# class ClassName(models.Model):
#   attr = models.[CharField(max_length=10)/TextFeild()/DateTimeField()/IntegerField()/ForeignKey/ManyTomMnyField()]

import requests
from math import radians, sin, cos, sqrt, atan2

# Helper function to calculate distance
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def get_coordinates_from_address(address):
    url = "https://www.als.gov.hk/lookup"
    params = {
        "q": address,  # Query parameter for the address
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # Parse XML response
        root = ET.fromstring(response.content)
        # Find Latitude and Longitude in the GeospatialInformation tag
        geospatial = root.find(".//GeospatialInformation")
        if geospatial is not None:
            latitude = float(geospatial.find("Latitude").text)
            longitude = float(geospatial.find("Longitude").text)
            geo_address = root.find(".//GeoAddress").text  # Optional: capture GeoAddress
            return latitude, longitude, geo_address
    return None, None, None  # Return None if no data found

class Accommodation(models.Model):
    accommodation_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    owner_details = models.CharField(max_length=100)
    available_from = models.DateTimeField()
    available_to = models.DateTimeField()
    bed_num = models.IntegerField()
    bedroom_num = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # In HKD
    distance_from_campus = models.FloatField(null=True, blank=True)  # In km, allow null initially
    latitude = models.FloatField(null=True, blank=True)  # Allow null initially
    longitude = models.FloatField(null=True, blank=True)  # Note: corrected typo "longtitude"
    geoAddress = models.CharField(null=True, blank=True, max_length=255)  # Note: corrected typo "geoAdrress"

    def update_location_data(self, campus_lat=22.2838, campus_lon=114.1360):
        """Update latitude, longitude, geoAddress, and distance_from_campus using ALS API."""
        lat, lon, geo_addr = get_coordinates_from_address(self.name)
        if lat and lon and geo_addr:
            self.latitude = lat
            self.longitude = lon
            self.geoAddress = geo_addr  # Update geoAddress with the API's GeoAddress
            self.distance_from_campus = calculate_distance(lat, lon, campus_lat, campus_lon)

    def save(self, *args, **kwargs):
        # Check if available_to is larger than available_from
        if self.available_to <= self.available_from:
            raise ValidationError('available_to must be later than available_from')
        # Update location data before saving if geoAddress is provided
        if self.name and (self.latitude is None or self.longitude is None):
            self.update_location_data()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class User(models.Model):
    user_id = models.IntegerField(primary_key=True) # Primary key
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class HKUStudent(User):
    HKU_ID = models.CharField(max_length=20, unique=True)

class CEDARSStaff(User):
    staff_id = models.CharField(max_length=20, unique=True)
    staff_department = models.CharField(max_length=100)

class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True) # Primary key
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # Foreign key
    accommodation_id = models.ForeignKey(Accommodation, on_delete=models.CASCADE) # Foreign key
    reservation_date = models.DateTimeField()
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    is_cancelled = models.BooleanField(default=False)

class CancelledReservation(models.Model):
    cancellation_id = models.AutoField(primary_key=True) # Primary key
    reservation_id = models.ForeignKey(Reservation, on_delete=models.CASCADE) # Foreign key
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # Foreign key [canncelled by user]

class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True) # Primary key
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # Foreign key
    type = models.CharField(max_length=100)
    notification_content = models.TextField()