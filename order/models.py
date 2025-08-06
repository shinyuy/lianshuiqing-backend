from django.db import models
from users.models import UserAccount
from django.conf import settings

ORDER_TYPE_CHOICES = [
    ('dine-in', 'Dine-In'),
    ('takeaway', 'Takeaway'),
    ('delivery', 'Delivery'),
]

ORDER_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('preparing', 'Preparing'),
    ('ready', 'Ready'),
    ('en_route', 'En Route'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders'  
    )
    branch = models.ForeignKey('branch.Branch', on_delete=models.SET_NULL, null=True, blank=True)

    type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES, default='dine-in')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

    table_number = models.CharField(max_length=20, blank=True, null=True)  # For dine-in

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='served_orders'
    )
    delivery_worker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='delivered_orders'
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username if self.user else 'Guest'}"


class GuestOrder(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    order = models.OneToOneField('Order', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
