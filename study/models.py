from django.db import models

from django.conf import settings

from config.settings import AUTH_USER_MODEL


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="название")
    preview = models.ImageField(upload_to="course/", verbose_name="Превью", null=True)
    description = models.TextField(verbose_name="описание")
    price = models.IntegerField(default=0, verbose_name="цена")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="создатель",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = [
            "title",
        ]


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    preview = models.ImageField(upload_to="lesson/", verbose_name="превью", null=True)
    link = models.CharField(max_length=300, verbose_name="ссылка")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="создатель",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["title"]


class Subscribe(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscribe")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscribe")
    is_active = models.BooleanField(default=False, verbose_name="Подписка")

    def __str__(self):
        return (
            f"{self.user} подписан на курс {self.course}"
            if self.is_active
            else f"{self.user} не подписан на курс {self.course}"
        )

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
        ordering = ["user", "course"]
