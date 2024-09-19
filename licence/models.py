from django.db import models

STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('revoked', 'Revoked')
    ]

class Licence(models.Model):
    issued_date = models.DateField()
    expiration_date = models.DateField()
    key = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    type = models.CharField(max_length=50, null=True, blank=True)  # License type (e.g., premium, trial)

    def __str__(self):
        return f'Licence {self.key} ({self.status})'


class Device(models.Model):
    first_login = models.DateTimeField()
    last_login = models.DateTimeField()
    mac = models.CharField(max_length=17, unique=True)  # MAC addresses have a fixed length
    device_name = models.CharField(max_length=100, null=True, blank=True)  # Optional: for identifying device
    licence = models.ForeignKey(Licence, on_delete=models.CASCADE)

    def __str__(self):
        return f'Device {self.mac} (Licence: {self.licence.key})'