from django.db import models
from users.models import UserAccount
from django.conf import settings
# from branch.models import Branch

class WaiterPoints(models.Model):
    waiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='points')
    points = models.IntegerField(default=0)
    branch = models.ForeignKey('branch.Branch', on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.waiter.username} - {self.points} pts"