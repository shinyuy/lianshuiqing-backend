from django.db import models
from users.models import UserAccount
from django.conf import settings
# from branch.models import Branch
from order.models import Order


class WaiterFeedback(models.Model):
    waiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks_received')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    branch = models.ForeignKey('branch.Branch', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.waiter.username} (Order #{self.order.id})"