from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(className)

class HKUStudentAdmin(admin.ModelAdmin):
    # Display common and subclass-specific fields
    list_display = ['user_id', 'username', 'email', 'HKU_ID']
    fields = ['username', 'password', 'email', 'HKU_ID']  # Include parent and subclass fields


class CEDARSStaffAdmin(admin.ModelAdmin):
    # Display common and subclass-specific fields
    list_display = ['user_id', 'username', 'email', 'staff_id', 'staff_department']
    fields = ['username', 'password', 'email', 'staff_id', 'staff_department']  # Include parent and subclass fields


admin.site.register(Accommodation)
admin.site.register(HKUStudent, HKUStudentAdmin)
admin.site.register(CEDARSStaff, CEDARSStaffAdmin)
admin.site.register(Reservation)
admin.site.register(CancelledReservation)