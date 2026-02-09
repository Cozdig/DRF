from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from study.models import Course, Lesson, Subscribe
from users.models import CustomUser


class LessonCRUDTestCase(APITestCase):

    def setUp(self):
        self.owner = CustomUser.objects.create_user(
            username="owner_user",
            email='owner@example.com',
            password='ownerpass123'
        )

        self.user = CustomUser.objects.create_user(
            username="regular_user",
            email='regular@example.com',
            password='userpass123'
        )

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description',
            owner=self.owner
        )

        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            link='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.owner
        )

        self.lesson_data = {
            'title': 'New Lesson',
            'description': 'New Lesson Description',
            'link': 'https://www.youtube.com/watch?v=new',
            'course': self.course.id
        }

    def test_lesson_create_unauthorized(self):
        url = reverse('study:lesson_create')
        response = self.client.post(url, self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_create_authorized(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse('study:lesson_create')
        response = self.client.post(url, self.lesson_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_retrieve(self):
        url = reverse('study:lesson_retrieve', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update_unauthorized(self):
        url = reverse('study:lesson_update', kwargs={'pk': self.lesson.pk})
        data = {'title': 'new Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_update_authorized(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse('study:lesson_update', kwargs={'pk': self.lesson.pk})
        data = {'title': 'new Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_unauthorized(self):
        url = reverse('study:lesson_delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_delete_authorized(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse('study:lesson_delete', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscribeTestCase(APITestCase):

    def setUp(self):
        self.owner = CustomUser.objects.create_user(
            username="owner_user",
            email='owner@example.com',
            password='ownerpass123'
        )

        self.user = CustomUser.objects.create_user(
            username="regular_user",
            email='user@example.com',
            password='userpass123'
        )

        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.owner
        )

        self.subscription_data = {'course_id': self.course.id}

    def test_subscribe_unauthorized(self):
        url = reverse('study:subscribe')
        response = self.client.post(url, self.subscription_data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_subscribe_add(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse('study:subscribe')
        response = self.client.post(url, self.subscription_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Подписка добавлена')

    def test_subscribe_remove(self):
        Subscribe.objects.create(
            user=self.owner,
            course=self.course
        )

        self.client.force_authenticate(user=self.owner)
        url = reverse('study:subscribe')
        response = self.client.post(url, self.subscription_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')