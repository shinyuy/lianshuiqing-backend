from django.db import models
from django.conf import settings

class GiftClaim(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gift_claims')
    gift_name = models.CharField(max_length=100)
    points_used = models.PositiveIntegerField()
    claimed_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey('branch.Branch', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} claimed {self.gift_name}"
