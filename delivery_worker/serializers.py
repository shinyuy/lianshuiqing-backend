from rest_framework import serializers
from .models import DeliveryAssignment


class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAssignment
        fields = '__all__'
