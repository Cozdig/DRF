from django.utils import timezone
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from users.models import CustomUser
from .models import Subscribe, Course


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscribe.objects.filter(course=course, is_active=True)

    if not subscribers.exists():
        return f"Нет подписчиков для курса {course.title}"

    recipient_list = [sub.user.email for sub in subscribers if sub.user.email]

    if not recipient_list:
        return "Нет email адресов для отправки"

    send_mail(
        subject=f'Обновление курса: {course.title}',
        message=f'Курс "{course.title}" был обновлен. Зайдите на сайт!',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    return f"Уведомление отправлено {len(recipient_list)} подписчикам курса {course.title}"


@shared_task
def deactivate_inactive_users():
        month_ago = timezone.now() - timedelta(days=30)
        inactive_users = CustomUser.objects.filter(
            is_active=True,
            last_login__lt=month_ago
        ).exclude(is_superuser=True).exclude(is_staff=True)

        count = inactive_users.count()

        if count > 0:
            inactive_users.update(is_active=False)
            return f"Деактивировано {count} пользователей"
        else:
            return "Нет пользователей для деактивации"
