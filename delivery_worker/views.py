from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Branch, FidelityCard, Order, WaiterFeedback, WaiterPoints, DeliveryAssignment
from .serializers import (
    BranchSerializer, FidelityCardSerializer, OrderSerializer,
    WaiterFeedbackSerializer, WaiterPointsSerializer, DeliveryAssignmentSerializer
)

# --- Delivery Assignment ---
class DeliveryAssignmentListCreateView(generics.ListCreateAPIView):
    queryset = DeliveryAssignment.objects.all()
    serializer_class = DeliveryAssignmentSerializer

class DeliveryAssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryAssignment.objects.all()
    serializer_class = DeliveryAssignmentSerializer