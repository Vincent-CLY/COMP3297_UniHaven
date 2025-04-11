from django.urls import path
from django.views.generic import RedirectView
from .api_views import list_accommodations, detailed_accommodation, create_reservation, cancel_reservation

urlpatterns = [
    path("", RedirectView.as_view(url="api/accommodations", permanent=False), name="home"),
    path("api/accommodations", list_accommodations.as_view(), name="list_accommodations"),
    path("api/accommodations/<int:pk>", detailed_accommodation.as_view(), name="accommodation_detail"),
    path("api/accommodations/reserve/<int:pk>", create_reservation.as_view(), name="accommodation_detail"),
    path("api/accommodations/cancel/", cancel_reservation.as_view(), name="accommodation_detail"),

]
