from rest_framework import serializers
from .models import FidelityCard


class FidelityCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FidelityCard
        fields = '__all__'
