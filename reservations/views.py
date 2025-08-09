from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import JsonResponse
from .models import Reservation
from .serializers import ReservationSerializer
from users.models import UserAccount

# GET all reservations for the authenticated user, and POST to create a new one
class ReservationApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            all_reservations = Reservation.objects.filter(customer=request.user).order_by('-created_at')
            serialized_reservations = ReservationSerializer(all_reservations, many=True).data

            return Response(serialized_reservations, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        try:
            user = UserAccount.objects.get(id=request.user.id)

            data = {
                'user': user.id,
                'branch': request.data.get('branch'),
                'dish': request.data.get('dish'),
                'date': request.data.get('date'),
                'time': request.data.get('time'),
                'guests': request.data.get('guests', 1),
                'notes': request.data.get('notes', ''),
            }

            serializer = ReservationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# GET a single reservation by ID
class ReservationDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            reservation = Reservation.objects.get(id=pk, user=request.user)
            serializer = ReservationSerializer(reservation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return JsonResponse({'error': 'Reservation not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# Cancel a reservation
class CancelReservationApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            reservation = Reservation.objects.get(id=pk, customer=request.user)

            if reservation.status == 'cancelled':
                return JsonResponse({'error': 'Reservation already cancelled'}, status=400)

            reservation.status = 'cancelled'
            reservation.save()

            return Response({'message': 'Reservation cancelled successfully'}, status=status.HTTP_200_OK)

        except Reservation.DoesNotExist:
            return JsonResponse({'error': 'Reservation not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
