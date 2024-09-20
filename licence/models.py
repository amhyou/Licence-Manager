from django.db import models
from datetime import timedelta, date
import uuid

STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked')
    ]

class Licence(models.Model):
    issued_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(blank=True)
    key = models.CharField(max_length=255, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    type = models.CharField(max_length=50, null=True, blank=True, default="trial")  # License type (e.g., premium, trial)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = str(uuid.uuid4())
        if not self.expiration_date:
            self.expiration_date = date.today() + timedelta(days=365)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Licence {self.key} ({self.status})'


class Device(models.Model):
    first_login = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    mac = models.CharField(max_length=17, unique=True)  # MAC addresses have a fixed length
    device_name = models.CharField(max_length=100, null=True, blank=True)  # Optional: for identifying device
    licence = models.ForeignKey(Licence, on_delete=models.CASCADE)

    def __str__(self):
        return f'Device {self.mac} (Licence: {self.licence.key})'