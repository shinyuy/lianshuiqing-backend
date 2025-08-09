from rest_framework import serializers
from .models import Reservation
from dish.serializers import DishSerializer

class ReservationSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
