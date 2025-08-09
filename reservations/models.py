from django.db import models
from django.conf import settings

RESERVATION_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

class Reservation(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    date = models.DateTimeField()
    number_of_people = models.PositiveIntegerField()
    special_request = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservation for {self.customer} on {self.date}"


class ReservationDish(models.Model):
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name='reservation_dishes'
    )
    dish = models.ForeignKey(
        'dish.Dish', on_delete=models.CASCADE, related_name='dish_reservations'
    )
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name} for Reservation {self.reservation.id}"

  