from django.db import models

class Dish(models.Model):
    CATEGORY_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('drink', 'Drink'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)   
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_available = models.BooleanField(default=True)
    branch = models.ForeignKey('branch.Branch', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.URLField(blank=False, null=False)

    def __str__(self):
        return f"{self.name} ({self.branch.name if self.branch else 'All branches'})"
