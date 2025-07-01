from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Branch
from .serializers import (
    BranchSerializer
)

# --- Branch ---
class BranchListCreateView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer