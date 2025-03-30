from django.db import models

# Create your models here.
# Define classes, each class has its properties, specify their attribute
#  !!! Relate to the UML Graph
# class ClassName(models.Model):
#   attr = models.[CharField(max_length=10)/TextFeild()/DateTimeField()/IntegerField()/ForeignKey/ManyTomMnyField()]

class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    is_avaliable = models.BooleanField(default=True)
    ownerDetails = models.CharField(max_length=100)
    available_from = models.DateTimeField()
    available_to = models.DateTimeField()
    bed_num = models.IntegerField()
    bedroom_num = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    distance_from_campus = models.FloatField()
    latitude = models.FloatField()
    longtitude = models.FloatField()
    geoAdrress = models.CharField()
