from django.db import models
from users.models import CustomUser

# Create your models here.

class Service(models.Model):
    """
    Predefined popular services (e.g., Netflix, Spotify, AWS) 
    to ensure clean UI icons and normalized data.
    """
    name = models.CharField(max_length=100, unique=True)
    logo_url = models.URLField(blank=True, null=True)
    is_custom = models.BooleanField(default=False, help_text="True if manually created by an individual user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False, help_text="Admin approval required for custom services")
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """
    Represents a user's subscription to a service, 
    including details like cost, billing cycle, and next billing date.
    """
    class BillingCycle(models.TextChoices):
        MONTHLY = 'MONTHLY', 'Monthly'
        YEARLY = 'YEARLY', 'Yearly'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        PAUSED = 'PAUSED', 'Paused'
        CANCELED = 'CANCELED', 'Canceled'
        EXPIRED = 'EXPIRED', 'Expired'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100, blank=True, null=True)  # e.g., "Premium", "Basic"
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=50, choices=BillingCycle.choices)  # e.g., "Monthly", "Yearly"
    next_billing_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_billing_date']

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"
    

class Budget(models.Model):
    """
    Represents a user's budget for subscriptions, 
    allowing them to set limits and track spending.
    """

    class Duration(models.TextChoices):
        MONTHLY = 'MONTHLY', 'Monthly'
        QUATERLY = 'QUARTERLY', 'Quarterly'
        SEMI_ANNUAL = 'SEMI_ANNUAL', 'Semi-Annual'
        YEARLY = 'YEARLY', 'Yearly'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='budget')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=20, choices=Duration.choices, default=Duration.MONTHLY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['amount']


    def __str__(self):
        return f"{self.user.username}'s Budget"
