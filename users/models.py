from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Город", null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
    ]

    def __str__(self):
        return self.email
