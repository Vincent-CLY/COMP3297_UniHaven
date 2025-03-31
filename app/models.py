from django.db import models

# Create your models here.
# Define classes, each class has its properties, specify their attribute
#  !!! Relate to the UML Graph
# class ClassName(models.Model):
#   attr = models.[CharField(max_length=10)/TextFeild()/DateTimeField()/IntegerField()/ForeignKey/ManyTomMnyField()]

class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    owner_details = models.CharField(max_length=100)
    available_from = models.DateTimeField()
    available_to = models.DateTimeField()
    bed_num = models.IntegerField()
    bedroom_num = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # In HKD
    distance_from_campus = models.FloatField() # In km
    latitude = models.FloatField()
    longtitude = models.FloatField()
    geoAdrress = models.CharField(max_length=255)

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