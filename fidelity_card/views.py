from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Branch, FidelityCard
from .serializers import (
  FidelityCardSerializer
)


# --- Fidelity Card ---
class FidelityCardListCreateView(generics.ListCreateAPIView):
    queryset = FidelityCard.objects.all()
    serializer_class = FidelityCardSerializer

class FidelityCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FidelityCard.objects.all()
    serializer_class = FidelityCardSerializer