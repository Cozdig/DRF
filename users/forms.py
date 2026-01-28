from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    avatar = forms.ImageField(help_text="Ваш аватар")
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        help_text="Необязательное поле. Введите ваш номер телефона.",
    )
    city = forms.CharField(max_length=100, help_text="Обязательное поле. Введите город")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "email",
            "avatar",
            "phone_number",
            "city",
            "password1",
            "password2",
        )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры.")
        return phone_number

    def clean_city(self):
        city = self.cleaned_data.get("city")
        if not city.isalpha():
            raise forms.ValidationError("Город может содержать только буквы")
        return city


# Форма авторизации
class CustomAuthenticationForm(AuthenticationForm):
    pass
