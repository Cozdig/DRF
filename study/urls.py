from django.urls import path
from rest_framework.routers import DefaultRouter

from study.views import CourseViewSet, LessonListCreateAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', LessonListCreateAPIView.as_view(), name='lesson_list_create'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
] + router.urls