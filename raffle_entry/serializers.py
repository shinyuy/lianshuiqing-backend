from rest_framework import serializers
from .models import RaffleEntry


class RaffleEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = RaffleEntry
        fields = '__all__'
