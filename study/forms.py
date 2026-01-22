from django import forms
from .models import Course, Lesson


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'preview']

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название'
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание'
        })

        self.fields['preview'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите превью'
        })

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'preview', 'link', 'course']

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название'
        }),

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание'
        }),

        self.fields['preview'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите превью'
        }),

        self.fields['link'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ссылку'
        }),

        self.fields['course'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите курс'
        })