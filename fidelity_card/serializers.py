from rest_framework import serializers
from .models import FidelityCard, FidelityCardSubscription


class FidelityCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FidelityCard
        fields = '__all__'
        
        
class FidelityCardSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FidelityCardSubscription
        fields = '__all__'


# from rest_framework import serializers
# from .models import FidelityCard
# from users.serializers import UserAccountSerializer
# from branch.serializers import BranchSerializer

# class FidelityCardSerializer(serializers.ModelSerializer):
#     user = UserAccountSerializer(read_only=True)
#     branch_issued = BranchSerializer(read_only=True)

#     class Meta:
#         model = FidelityCard
#         fields = ['id', 'user', 'branch_issued', 'card_type', 'issued_at', 'expires_at']