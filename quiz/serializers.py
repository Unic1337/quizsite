from user.models import Profile

from rest_framework import serializers, status

from .models import Quiz, QuizResult


class QuizSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Quiz
        fields = ("id", "title", "creator", "quiz_img_url", "creation_time", "change_time", "questions")


class QuizResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizResult
        fields = ("quiz_id", "creation_time", "quiz_result")
