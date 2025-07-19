from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Branch, FidelityCard
from .serializers import (
  FidelityCardSerializer
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import JsonResponse
from users.models import UserAccount
from .serializers import FidelityCardSerializer

class FidelityCardApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        
        try:
            # user = request.user
            card_type = request.data.get('name')
            branch_id = request.data.get('branch')
            points_required = request.data.get('pointsRequired')
            reward = request.data.get('reward')

            if not card_type:
                return JsonResponse({'error': 'Card type is required.'}, status=400)

            if card_type not in dict(FidelityCard.CARD_CHOICES):
                return JsonResponse({'error': 'Invalid card type.'}, status=400)

            branch = None
            if branch_id:
                try:
                    branch = Branch.objects.get(id=branch_id)
                except Branch.DoesNotExist:
                    return JsonResponse({'error': 'Branch not found.'}, status=404)

            fidelity_card = FidelityCard.objects.create(
                # user=user,
                branch_issued=branch,
                card_type=card_type,
                points_required=points_required,
                reward=reward
            )

            serializer = FidelityCardSerializer(fidelity_card)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
          
          
    def get(self, request, *args, **kwargs):
        try:
            cards = FidelityCard.objects.all()
            serializer = FidelityCardSerializer(cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)        
          

class DeleteFidelityCardApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            card_id = kwargs.get('id')  # ✅ Get ID from URL, not from query params

            if not card_id:
                return JsonResponse({'error': 'Card ID is required.'}, status=400)

            try:
                card = FidelityCard.objects.get(id=card_id)
            except FidelityCard.DoesNotExist:
                return JsonResponse({'error': 'Card not found.'}, status=404)

            card.delete()
            return JsonResponse({'message': 'Card deleted successfully.'}, status=204)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)          