import uuid

from django.db import models

# Create your models here.
from django.utils import timezone

DISABLED = 'DISABLED'
SENIOR = 'SENIOR'

STATUS_CHOICES = ((DISABLED, 'DISABLED'), (SENIOR, 'SENIOR'))


class UserNotification(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=1000)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.mobile)

    class Meta:
        verbose_name = 'User Notification'


class Otp(models.Model):
    user = models.OneToOneField(UserNotification, on_delete=models.CASCADE)
    otp = models.IntegerField()
    generated_at = models.DateTimeField(auto_now_add=True)


class UserCategory(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user = models.OneToOneField(UserNotification, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'User Category'
        verbose_name_plural = 'User Categories'


class BulkMessageIssuer(models.Model):
    issuer = models.ForeignKey(UserNotification, on_delete=models.CASCADE)
    message = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=15, choices=STATUS_CHOICES)


class TokenIssuer(models.Model):
    active_user = models.OneToOneField(UserNotification, on_delete=models.CASCADE)
    token = models.CharField(max_length=1000)


