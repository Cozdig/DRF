from rest_framework import serializers


class LinkLessonValidator:
    def __call__(self, value):
        if "youtube" not in value:
            raise serializers.ValidationError("Ссылки могут быть только с youtube")
