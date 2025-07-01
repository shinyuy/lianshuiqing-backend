from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import RaffleWinner
from .serializers import RaffleWinnerSerializer

# RaffleWinner Views
class RaffleWinnerListCreateView(generics.ListCreateAPIView):
    queryset = RaffleWinner.objects.all()
    serializer_class = RaffleWinnerSerializer
    permission_classes = [IsAuthenticated]

class RaffleWinnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RaffleWinner.objects.all()
    serializer_class = RaffleWinnerSerializer
    permission_classes = [IsAuthenticated]