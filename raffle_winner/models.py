from django.db import models
from django.conf import settings

# Create your models here.
class RaffleWinner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='raffle_wins')
    raffle_name = models.CharField(max_length=100)
    won_at = models.DateTimeField(auto_now_add=True)
    prize_description = models.CharField(max_length=255)
    branch = models.ForeignKey('branch.Branch', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} won {self.raffle_name}"
