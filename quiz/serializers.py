from rest_framework import serializers

from .models import Quiz, QuizResult


class QuizSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Quiz
        fields = ("id", "title", "creator", "quiz_img_url", "creation_time", "change_time", "questions",)


class QuizResultSerializer(serializers.ModelSerializer):
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = QuizResult
        fields = ("user_id", "quiz_id", "creation_time", "quiz_result",)
