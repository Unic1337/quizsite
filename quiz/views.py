from rest_framework import status, generics
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.settings import api_settings

from quiz.models import Quiz, QuizResult
from quiz.permissions import IsOwnerOrReadOnly
from quiz.serializers import QuizSerializer, QuizResultSerializer


class QuizAPIList(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class QuizAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        quiz = serializer.data
        quiz["quiz_results"] = []

        for result in QuizResult.objects.filter(quiz_id=instance.id):
            quiz["quiz_results"].append(QuizResultSerializer(result).data)
        return Response(quiz)


class QuizAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class QuizResultAPIList(generics.ListCreateAPIView):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.create_result(serializer.validated_data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data["quiz_result"], status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def create_result(self, data):
        correct_answers = [question["correct"] for question in data["quiz_id"].questions]
        user_answers = data.get("quiz_result")
        quiz_result = {"final_result": 0, "answers_results": []}

        for i in range(0, len(user_answers)):
            if user_answers[i] == correct_answers[i]:
                quiz_result["final_result"] += 1
            quiz_result["answers_results"].append([user_answers[i], user_answers[i] == correct_answers[i]])

        quiz_result['final_result'] /= len(correct_answers)
        data["quiz_result"] = quiz_result
