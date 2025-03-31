from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(className)

admin.site.register(Accommodation)
admin.site.register(User)
admin.site.register(Reservation)
admin.site.register(CancelledReservation)