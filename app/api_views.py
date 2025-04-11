from rest_framework import generics, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AccommodationFilter
from .models import Accommodation, Reservation, CancelledReservation, Rating
from .serializers import SimpleAccommodationSerializer, DetailedAccommodationSerializer, ReservationSerializer, CancelledReservationSerializer, NotificationSerializer, RatingSerializer

class list_accommodations(generics.ListAPIView):
    queryset = Accommodation.objects.filter(is_available="True")
    serializer_class = SimpleAccommodationSerializer
    filterset_class = AccommodationFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']

class detailed_accommodation(generics.RetrieveAPIView):
    queryset = Accommodation.objects.filter(is_available="True")
    serializer_class = DetailedAccommodationSerializer

class create_reservation(generics.GenericAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def post(self, request, accommodation_id, *args, **kwargs):
        try:
            user_id = request.data.get("user_id")
            reservation_date = request.data.get("reservation_date")
            check_in_date = request.data.get("check_in_date")
            check_out_date = request.data.get("check_out_date")

            if not user_id or not reservation_date or not check_in_date or not check_out_date:
                return Response(
                    {
                        "error": "user_id, reservation_date, check_in_date and check_out_date are required."
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

            try:
                user_id = int(user_id)
            except ValueError:
                return Response(
                    {
                        "error": "user_id must be an integer."
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

            # Check if the accommodation exists
            try:
                accommodation = Accommodation.objects.filter(accommodation_id=accommodation_id).first()
            except Accommodation.DoesNotExist:
                return Response(
                    {
                        "error": "Accommodation not found."
                    },
                    status = status.HTTP_404_NOT_FOUND
                )

            # Create a new reservation
            reservation_data = {
                "user_id": user_id,
                "accommodation_id": accommodation_id,
                "reservation_date": reservation_date,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "is_cancelled": False
            }
            serializer = self.get_serializer(data=reservation_data)
            serializer.is_valid(raise_exception=True)
            reservation_record = serializer.save()

            # Update the accommodation's availability
            accommodation.is_available = False
            accommodation.save()

            notification_data = {
                "user_id" : reservation_record.user_id.user_id,
                "type" : "Reservation",
                "notification_content" : f"Your reservation of {accommodation.name} has been created successfully."
            }
            notification_serializer = NotificationSerializer(data=notification_data)
            notification_serializer.is_valid(raise_exception=True)
            notification_record = notification_serializer.save()

            return Response(
                {
                    "reservation" : ReservationSerializer(reservation_record).data,
                    "notification" : NotificationSerializer(notification_record).data
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error" : str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

class cancel_reservation(generics.GenericAPIView):
    queryset = CancelledReservation.objects.all()
    serializer_class = CancelledReservationSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request, reservation_id, *args, **kwargs):
        try:
            user_id = request.data.get("user_id")

            if not user_id:
                return Response(
                    {
                        "error": "user_id is required."
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

            try:
                user_id = int(user_id)
            except ValueError:
                return Response(
                    {
                        "error": "user_id must be an integer."
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

            # reservation = Reservation.objects.get(pk=pk)
            try:
                reservation = Reservation.objects.filter(reservation_id=reservation_id).first()
            except Reservation.DoesNotExist:
                return Response(
                    {
                        "error": "Reservation not found."
                    },
                    status = status.HTTP_404_NOT_FOUND
                )

            if user_id != reservation.user_id.user_id:
                return Response(
                    {
                        "error": "You do not have access to this reservation."
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

            cancelled_data = {
                "reservation_id" : reservation_id,
                "user_id" : user_id
            }
            cancelled_serializer = CancelledReservationSerializer(data=cancelled_data)
            cancelled_serializer.is_valid(raise_exception=True)
            cancelled_record = cancelled_serializer.save()
            # if user_id != reservation.user_id.user_id: # The user_id is not defined
            #         return Response(
            #         {
            #             "error": "You do not have access to this reservation."
            #         },
            #         status = status.HTTP_400_BAD_REQUEST
            #     )
            # print(f"Accommodation_id: {reservation.accommodation_id.accommodation_id}")
            # print(f"Reservation: {reservation.reservation_id}")
            try:
                accommodation = Accommodation.objects.filter(accommodation_id=reservation.accommodation_id.accommodation_id).first()
            except Accommodation.DoesNotExist:
                return Response(
                    {
                        "error": "Accommodation not found."
                    },
                    status = status.HTTP_404_NOT_FOUND
                )
            
            if reservation.is_cancelled: # Prevent extra cancel on the same reservation
                return Response(
                    {
                        "error" : f"The reservation of {accommodation.name} has already been cancelled."
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

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

class rate_accommodation(generics.GenericAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def post(self, request, accommodation_id, *args, **kwargs):
        try:
            user_id = request.data.get("user_id")
            score = request.data.get("score")

            if not user_id or not score:
                return Response(
                    {
                        "error": "user_id and score are required."
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

            try:
                user_id = int(user_id)
                score = int(score)
            except ValueError:
                return Response(
                    {
                        "error": "user_id and score must be integers"
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

            # Check if the accommodation exists
            try:
                accommodation = Accommodation.objects.filter(accommodation_id=accommodation_id).first()
            except Accommodation.DoesNotExist:
                return Response(
                    {
                        "error": "Accommodation not found."
                    },
                    status = status.HTTP_404_NOT_FOUND
                )

            # Check if the user has already rated this accommodation
            existing_rating = Rating.objects.filter(accommodation_id=accommodation, user_id=user_id).first()
            if existing_rating:
                existing_rating.score = score
                existing_rating.save()
                return Response(
                    {
                        "message": f"Rating to {accommodation.name} has been updated to {existing_rating.score} successfully.",
                    },
                    status = status.HTTP_200_OK
                )

            # Create a new rating
            rating_data = {
                "accommodation_id": accommodation_id,
                "user_id": user_id,
                "score": score
            }
            serializer = self.get_serializer(data=rating_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # Update the accommodation's average rating
            ratings = Rating.objects.filter(accommodation_id=accommodation)
            avg_rating = sum(rating.score for rating in ratings) / len(ratings)
            accommodation.avg_rating = avg_rating
            accommodation.save()

            return Response(
                {
                    "rating": serializer.data,
                    "average_rating": avg_rating
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error" : str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
        
