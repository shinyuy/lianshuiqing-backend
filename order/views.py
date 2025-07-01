from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Order
from .serializers import (
    OrderSerializer
)


# --- Orders ---
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
