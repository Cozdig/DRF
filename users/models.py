from django.db import models
from django.contrib.auth.models import AbstractUser

from study.models import Course, Lesson


# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField(unique=True, verbose_name="имя пользователя")

    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="Город", null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Payments(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("card", "Card"),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payments")

    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="дата оплаты")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="payments", null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="payments", null=True)
    payment_method = models.CharField(
        max_length=4,
        choices=PAYMENT_METHOD_CHOICES,
        null=False,
        verbose_name="способ оплаты",
    )

    def __str__(self):
        return f"{self.payment_date} -- {self.user}"

    class Meta:
        verbose_name = "оплата"
        verbose_name_plural = "оплата"
        ordering = [
            "-payment_date",
        ]
