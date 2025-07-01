from rest_framework import serializers
from .models import GiftClaim

class GiftClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftClaim
        fields = '__all__'