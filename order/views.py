from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import JsonResponse
from .models import Order
from .serializers import OrderSerializer
from users.models import UserAccount

# GET all orders for the authenticated user, and POST to create a new one
class OrderApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            all_orders = Order.objects.all().order_by('-created_at')
            serialized_orders = OrderSerializer(all_orders, many=True).data

            return Response(serialized_orders, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        try:
            user = UserAccount.objects.get(id=request.user.id)

            data = {
                'user': user.id,
                'branch': request.data.get('branch'),
                'waiter': request.data.get('waiter'),
                'delivery_worker': request.data.get('delivery_worker'),
            }

            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except UserAccount.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# GET a single order by ID (authenticated user)
class OrderDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(id=pk, user=request.user)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# Cancel an order (mark as cancelled)
class CancelOrderApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(id=pk, user=request.user)

            if order.status == 'cancelled':
                return JsonResponse({'error': 'Order already cancelled'}, status=400)

            order.status = 'cancelled'
            order.save()

            return Response({'message': 'Order cancelled successfully'}, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
