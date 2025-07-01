from rest_framework import serializers
from .models import  WaiterFeedback


class WaiterFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaiterFeedback
        fields = '__all__'
