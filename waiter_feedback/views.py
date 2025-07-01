from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import WaiterFeedback
from .serializers import (
    WaiterFeedbackSerializer
)

# --- Waiter Feedback ---
class WaiterFeedbackListCreateView(generics.ListCreateAPIView):
    queryset = WaiterFeedback.objects.all()
    serializer_class = WaiterFeedbackSerializer

class WaiterFeedbackDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WaiterFeedback.objects.all()
    serializer_class = WaiterFeedbackSerializer
