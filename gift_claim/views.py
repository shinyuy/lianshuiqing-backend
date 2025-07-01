from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import GiftClaim
from .serializers import GiftClaimSerializer


# GiftClaim Views
class GiftClaimListCreateView(generics.ListCreateAPIView):
    queryset = GiftClaim.objects.all()
    serializer_class = GiftClaimSerializer
    permission_classes = [IsAuthenticated]

class GiftClaimDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GiftClaim.objects.all()
    serializer_class = GiftClaimSerializer
    permission_classes = [IsAuthenticated]