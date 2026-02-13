import stripe
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Payments
from .models import Course, Lesson, Subscribe
from .paginations import Pagination
from .permissions import IsManager, IsOwner
from .serializers import CourseSerializer, LessonSerializer
from config.settings import STRIPE_SECRET_KEY

# Create your views here.
stripe.api_key = STRIPE_SECRET_KEY

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


class CreateStripeCourseView(APIView):
    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)

        product = stripe.Product.create(
            name=course.title,
            description=course.description,
        )

        price = stripe.Price.create(
            product=product.id,
            unit_amount=course.price * 100,
            currency='rub'
        )

        return Response({'price_id': price.id, 'product_id': product.id})


class CreateCheckoutSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        price_id = request.data.get('price_id')
        course_id = request.data.get('course_id')
        lesson_id = request.data.get('lesson_id')

        if not price_id:
            return Response(
                {"error": "Необходимо указать price_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not course_id and not lesson_id:
            return Response(
                {"error": "Необходимо указать course_id или lesson_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if course_id:
            course = get_object_or_404(Course, id=course_id)
            lesson = None
            amount = course.price
            title = course.title
            item_type = 'курс'
            item_id = course_id
        else:
            lesson = get_object_or_404(Lesson, id=lesson_id)
            course = lesson.course
            amount = lesson.price
            title = lesson.title
            item_type = 'урок'
            item_id = lesson_id

        if not amount:
            return Response(
                {"error": f"У {item_type}а не указана цена"},
                status=status.HTTP_400_BAD_REQUEST
            )

        checkout_session = stripe.checkout.Session.create(
            success_url='http://127.0.0.1:8000/success',
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            metadata={
                'item_type': item_type,
                'item_id': str(item_id),
                'user_id': str(request.user.id),
                'item_title': title,
                'amount': str(amount)
            }
        )

        payment = Payments.objects.create(
            user=request.user,
            course=course,
            lesson=lesson,
            amount=amount,
            payment_method='card',
            stripe_session_id=checkout_session.id,
            checkout_url=checkout_session.url,
            stripe_payment_id=checkout_session.payment_intent
        )

        return Response({
            'checkout_url': checkout_session.url,
            'session_id': checkout_session.id,
            'payment_id': payment.id,
            'amount': str(amount),
            'item_type': item_type,
            'item_title': title
        })