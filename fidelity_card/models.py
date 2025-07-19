from django.db import models
from users.models import UserAccount
from django.conf import settings
from branch.models import Branch

class FidelityCard(models.Model):
    CARD_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ]

    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fidelity_cards')
    branch_issued = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    card_type = models.CharField(max_length=10, choices=CARD_CHOICES)
    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    points_required = models.PositiveIntegerField(default=0)
    reward = models.CharField(null=False, blank=False)

    def __str__(self):
        return f"{self.card_type.title()} Card for {self.user.username}"