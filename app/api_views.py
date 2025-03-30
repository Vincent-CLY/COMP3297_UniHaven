from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
from .models import Accommodation
from .serializers import SimpleAccommodationSerializer, DetailedAccommodationSerializer

# @api_view(['GET', ])
# def list_all_accommodations(request):
#     accommodations = Accommodation.objects.all()
#     accommodations_serializer = AccommodationSerializer(accommodations, many=True)
#     return Response(accommodations_serializer.data)

class all_available_accommodations(generics.ListAPIView):
    queryset = Accommodation.objects.filter(is_available="True")
    serializer_class = SimpleAccommodationSerializer

class detailed_accommodation(generics.RetrieveAPIView):
    queryset = Accommodation.objects.all()
    serializer_class = DetailedAccommodationSerializer
