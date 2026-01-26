from django.db import models


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="название")
    preview = models.ImageField(upload_to="course/", verbose_name="Превью")
    description = models.TextField(verbose_name="описание")

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
    preview = models.ImageField(upload_to="lesson/", verbose_name="превью")
    link = models.CharField(max_length=300, verbose_name="ссылка")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["title"]
