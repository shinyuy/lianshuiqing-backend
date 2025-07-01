from rest_framework import serializers
from .models import RaffleWinner

class RaffleWinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaffleWinner
        fields = '__all__'
