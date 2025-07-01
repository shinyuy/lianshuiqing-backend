from rest_framework import serializers
from .models import WaiterPoints


class WaiterPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaiterPoints
        fields = '__all__'