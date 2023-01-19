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
        correct_answers = {str(question.get("id")): question.get("correct") for question in data["quiz_id"].questions}
        user_answers = data.get("quiz_result")
        quiz_result = {"final_result": 0, "answers_results": {}}

        for i in range(1, len(correct_answers)+1):
            try:
                if user_answers[str(i)] == correct_answers[str(i)]:
                    quiz_result["final_result"] += 1
                quiz_result.get("answers_results").update({i: [user_answers[str(i)],
                                                               user_answers[str(i)] == correct_answers[str(i)]]})
            except IndexError:
                pass

        data["quiz_result"] = quiz_result
