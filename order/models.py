from django.db import models
from users.models import UserAccount
from django.conf import settings
# from branch.models import Branch

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    branch = models.ForeignKey('branch.Branch', on_delete=models.SET_NULL, null=True, blank=True)
    waiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='served_orders')
    delivery_worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivered_orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"