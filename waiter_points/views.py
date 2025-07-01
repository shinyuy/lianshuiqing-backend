from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import WaiterPoints
from .serializers import (
    WaiterPointsSerializer
)


# --- Waiter Points ---
class WaiterPointsListCreateView(generics.ListCreateAPIView):
    queryset = WaiterPoints.objects.all()
    serializer_class = WaiterPointsSerializer

class WaiterPointsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WaiterPoints.objects.all()
    serializer_class = WaiterPointsSerializer