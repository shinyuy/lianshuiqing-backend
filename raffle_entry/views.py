from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import RaffleEntry
from .serializers import RaffleEntrySerializer

# RaffleEntry Views
class RaffleEntryListCreateView(generics.ListCreateAPIView):
    queryset = RaffleEntry.objects.all()
    serializer_class = RaffleEntrySerializer
    permission_classes = [IsAuthenticated]

class RaffleEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RaffleEntry.objects.all()
    serializer_class = RaffleEntrySerializer
    permission_classes = [IsAuthenticated]