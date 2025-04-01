from django_filters import rest_framework as filters
from .models import Accommodation

class AccommodationFilter(filters.FilterSet):
    price = filters.RangeFilter()
    available_from = filters.DateTimeFilter(lookup_expr="lte")
    available_to = filters.DateTimeFilter(lookup_expr="gte")

    class Meta:
        model = Accommodation
        fields = ['name', 'type', 'owner_details', 'available_from', 'available_to', 'bed_num', 'bedroom_num', 'price', 'distance_from_campus', 'latitude', 'longitude', 'geoAddress']