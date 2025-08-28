from django.db import models
from django.conf import settings
from branch.models import Branch
from django.utils import timezone
from datetime import timedelta


class FidelityCard(models.Model):
    CARD_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    ]

    card_type = models.CharField(max_length=10, choices=CARD_CHOICES, unique=True)
    description = models.TextField(blank=True, help_text="Details of benefits for this card type")
    branch_issued = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)

    # Dynamic thresholds
    monthly_order_requirement = models.PositiveIntegerField(default=0, help_text="Orders required per month")
    six_month_points_requirement = models.PositiveIntegerField(default=0, help_text="Points required in 6 months")

    # Card pricing & rewards
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    renewal_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reward = models.CharField(max_length=255, blank=True, help_text="Gift given upon subscription")

    # Raffle spots
    raffle_spots = models.PositiveIntegerField(default=1, help_text="Number of raffle entries this card gives")

    # Subscription validity
    duration_days = models.PositiveIntegerField(default=365, help_text="Duration in days before expiry")

    def __str__(self):
        return f"{self.card_type.title()} Card"

    def default_expiry_date(self):
        return timezone.now() + timedelta(days=self.duration_days)


class FidelityCardSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='card_subscriptions')
    fidelity_card = models.ForeignKey(FidelityCard, on_delete=models.CASCADE, related_name='subscriptions')

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    # Track user activity
    monthly_orders = models.PositiveIntegerField(default=0, help_text="Orders this month")
    six_month_points = models.PositiveIntegerField(default=0, help_text="Total points in last 6 months")

    # Payment info
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)  
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.fidelity_card.duration_days)
        super().save(*args, **kwargs)

    def meets_requirements(self):
        """Check if user meets the fidelity requirements based on card type"""
        return (
            self.monthly_orders >= self.fidelity_card.monthly_order_requirement and
            self.six_month_points >= self.fidelity_card.six_month_points_requirement
        )
        
    def add_order(self):
        """Increment counters when a new eligible order is placed"""
        self.monthly_orders += 1
        self.six_month_points += 1
        self.save()

    def reset_monthly_orders_if_needed(self):
        """Reset monthly orders if new month started"""
        if self.start_date.month != timezone.now().month:
            self.monthly_orders = 0
            self.save()
        

    def __str__(self):
        return f"{self.user.email} - {self.fidelity_card.card_type} ({self.status})"
