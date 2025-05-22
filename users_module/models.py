from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='tenant')
    age = models.PositiveIntegerField(null=True, blank=True)
    about = models.TextField(blank=True, null=True)  # Field for bio or property description
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    hashtags = models.CharField(max_length=255, blank=True, null=True, help_text='Comma-separated hashtags')
    orientation = models.CharField(max_length=50, blank=True, null=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.user_type})"
