from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Lesson, Subscribe
from .paginations import Pagination
from .permissions import IsManager, IsOwner
from .serializers import CourseSerializer, LessonSerializer

# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = Pagination

    def get(self, request):
        queryset = Course.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == "list":
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == "retrieve":
            self.permission_classes = [permissions.IsAuthenticated]
        elif self.action == "update":
            self.permission_classes = [IsManager | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [IsOwner]
        return [permission() for permission in self.permission_classes]


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]
    pagination_class = Pagination


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsManager | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class SubscribeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")

        course = get_object_or_404(Course, id=course_id)

        subs_item = Subscribe.objects.filter(user=user, course=course)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            Subscribe.objects.create(user=user, course=course)
            message = "Подписка добавлена"
            return Response({"message": message}, status=status.HTTP_201_CREATED)
