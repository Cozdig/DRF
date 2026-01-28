from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from config import settings
from .forms import CustomUserCreationForm
from .models import Payments, CustomUser
from .serializers import PaymentsSerializer, CustomUserSerializer


# Create your views here.


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("study:home")

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать на наш сервис"
        message = "Спасибо за регистрацию"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [
            user_email,
        ]
        send_mail(subject, message, from_email, recipient_list)

class PaymentsListAPIView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('payment_date', 'course', 'lesson', 'payment_method')


class CustomUserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomUserUpdateAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomUserDestroyAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]