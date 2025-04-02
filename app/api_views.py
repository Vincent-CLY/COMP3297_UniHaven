from rest_framework import generics, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AccommodationFilter
from .models import Accommodation, Reservation, CancelledReservation
from .serializers import SimpleAccommodationSerializer, DetailedAccommodationSerializer, ReservationSerializer, CancelledReservationSerializer, NotificationSerializer

class list_accommodations(generics.ListAPIView):
    queryset = Accommodation.objects.filter(is_available="True")
    serializer_class = SimpleAccommodationSerializer
    filterset_class = AccommodationFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']


class detailed_accommodation(generics.RetrieveAPIView):
    queryset = Accommodation.objects.filter(is_available="True")
    serializer_class = DetailedAccommodationSerializer

class create_reservation(generics.CreateAPIView):
    model = Reservation
    serializer_class = ReservationSerializer

class cancel_reservation(generics.GenericAPIView):
    queryset = CancelledReservation.objects.all()
    serializer_class = CancelledReservationSerializer

    def post(self, request, pk, *args, **kwargs):
        try:
            reservation = Reservation.objects.get(pk=pk)
            print(f"Reservation: {reservation.reservation_id}")
            accommodation = Accommodation.objects.get(accommodation_id=reservation.accommodation_id.accommodation_id)
            if reservation.is_cancelled:
                return Response(
                    {
                        "error" : f"The reservation of {accommodation.name} has already been cancelled."
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )
            # print(f"Accommodation ID: {Accommodation.objects.get(accommodation_id=reservation.accommodation_id).accommodation_id}")
            # print(f"Accommodation name: {Accommodation.objects.get(accommodation_id=reservation.accommodation_id).name}")
            cancelled_data = {
                "reservation_id" : reservation.reservation_id,
                "user_id" : reservation.user_id.user_id
            }
            cancelled_serializer = CancelledReservationSerializer(data=cancelled_data)
            cancelled_serializer.is_valid(raise_exception=True)
            cancelled_record = cancelled_serializer.save()

            notification_data = {
                "user_id" : reservation.user_id.user_id,
                "type" : "Cancel",
                "notification_content" : f"Your reservation of {accommodation.name} has been cancelled."
            }
            notification_serializer = NotificationSerializer(data=notification_data)
            notification_serializer.is_valid(raise_exception=True)
            notification_record = notification_serializer.save()

            reservation.is_cancelled = True
            reservation.save()

            return Response(
                {
                    "cancelled_reservation" : CancelledReservationSerializer(cancelled_record).data,
                    "notification" : NotificationSerializer(notification_record).data,
                    "reservation_update" : {
                        "id" : reservation.reservation_id,
                        "is_cancelled" : reservation.is_cancelled
                    }
                },
                status = status.HTTP_201_CREATED,
            )
        except Reservation.DoesNotExist:
            return Response(
                {"error" : "Reservation not found."},
                status = status.HTTP_404_NOT_FOUND,
            )



    
        
