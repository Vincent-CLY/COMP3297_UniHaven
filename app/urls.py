from django.urls import path
from .api_views import all_available_accommodations, detailed_accommodation

urlpatterns = [
    path("api/accommodations", all_available_accommodations.as_view(), name="all_available_accommodations"),
    path("api/accommodations/<int:pk>", detailed_accommodation.as_view(), name="accommodation_detail"),

]
