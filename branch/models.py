from django.db import models
from users.models import UserAccount


class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)  # e.g., Bastos, Bonapriso
    opening_hours = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    manager = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_branches')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.location}"