# orders/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Order
from fidelity_card.models import FidelityCardSubscription


@receiver(pre_save, sender=Order)
def track_previous_status(sender, instance, **kwargs):
    """
    Before saving, store the old status so we can detect changes later.
    """
    if instance.pk:
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Order.DoesNotExist:
            instance._old_status = None


@receiver(post_save, sender=Order)
def update_fidelity_subscription(sender, instance, created, **kwargs):
    """
    When an order is marked delivered, update user's fidelity subscription counters.
    If status changes away from delivered, deduct the order.
    """
    if not instance.user:
        return  # skip guest orders

    try:
        subscription = FidelityCardSubscription.objects.filter(
            user=instance.user,
            status="active",
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        ).first()
    except FidelityCardSubscription.DoesNotExist:
        return

    if not subscription:
        return

    subscription.reset_monthly_orders_if_needed()

    # Case 1: order newly delivered
    if instance.status == "delivered" and getattr(instance, "_old_status", None) != "delivered":
        subscription.add_order()

    # Case 2: order status moved away from delivered
    elif getattr(instance, "_old_status", None) == "delivered" and instance.status != "delivered":
        subscription.remove_order()


@receiver(post_save, sender=FidelityCardSubscription)
def auto_downgrade_or_expire(sender, instance, **kwargs):
    """
    Auto downgrade or expire fidelity subscription if monthly requirements not met.
    Runs whenever subscription is saved.
    """
    instance.reset_monthly_orders_if_needed()

    # Check if we are past the subscription's end date
    if instance.end_date and timezone.now().date() > instance.end_date.date():
        instance.status = "expired"
        instance.save(update_fields=["status"])
        return

    # Check if the user failed to meet monthly orders
    if instance.monthly_orders_count < instance.required_monthly_orders:
        # simple version: downgrade to bronze OR expire
        if instance.card_type == "gold":
            instance.card_type = "silver"
        elif instance.card_type == "silver":
            instance.card_type = "bronze"
        else:
            instance.status = "expired"

        instance.save(update_fields=["status", "card_type"])
