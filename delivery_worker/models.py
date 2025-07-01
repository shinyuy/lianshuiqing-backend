from django.db import models
from django.db import models
from users.models import UserAccount
from django.conf import settings
from branch.models import Branch
from order.models import Order

# Create your models here.
class DeliveryAssignment(models.Model):
    delivery_worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignments')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery #{self.order.id} by {self.delivery_worker.username}"