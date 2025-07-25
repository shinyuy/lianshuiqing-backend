from rest_framework import serializers
from .models import Dish

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


# from rest_framework import serializers
# from .models import Dish

# class DishSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Dish
#         fields = ['id', 'owner', 'name', 'category', 'price', 'image', 'tags']
#         read_only_fields = ['id', 'owner']