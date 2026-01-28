from django.core.management.base import BaseCommand
from study.models import Course, Lesson
from users.models import CustomUser, Payments

class Command(BaseCommand):
    help = 'Add test data in database'

    def handle(self, *args, **kwargs):

        user, _ = CustomUser.objects.get_or_create(
            email='test@example.com',
            defaults={'first_name': 'Тест', 'last_name': 'Тестов', 'city': 'Москва'}
        )
        user.set_password('test123')
        user.save()

        course, _ = Course.objects.get_or_create(
            title='Тестовый курс',
            defaults={'description': 'Описание тестового курса'}
        )

        lesson, _ = Lesson.objects.get_or_create(
            title='Тестовый урок',
            course=course,
            defaults={'description': 'Описание урока', 'link': 'https://example.com'}
        )

        Payments.objects.get_or_create(user=user, course=course, payment_method='card')
        Payments.objects.get_or_create(user=user, lesson=lesson, payment_method='cash')

        self.stdout.write(self.style.SUCCESS('Тестовые данные созданы'))