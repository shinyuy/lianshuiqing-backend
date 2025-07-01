from django.db import models
from django.conf import settings

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mobile_money', 'Mobile Money'),
        ('card', 'Card'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey('order.Order', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} ({self.method})"
