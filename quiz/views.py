from rest_framework import status, generics
from rest_framework.permissions import *
from rest_framework.response import Response

from quiz.models import Quiz, QuizResult
from quiz.permissions import IsOwnerOrReadOnly
from quiz.serializers import QuizSerializer, QuizResultSerializer


class QuizAPIList(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class QuizAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        quiz = serializer.data

        quiz["quiz_results"] = []
        for result in instance.quizresult_set.all().select_related("user_id"):
            username = result.user_id.username
            result = QuizResultSerializer(result).data
            result.update({"username": username})
            quiz["quiz_results"].append(result)

        return Response(quiz)


class QuizResultAPIList(generics.ListCreateAPIView):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.create_result(serializer.validated_data)

        if not serializer.validated_data.get('user_id').id:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data["quiz_result"], status=status.HTTP_200_OK, headers=headers)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data["quiz_result"], status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def create_result(data):
        def make_lower_register(arr):
            if isinstance(arr, list):
                return [i.lower() if not isinstance(i, list) else [j.lower() for j in i] for i in arr]
            return arr

        quiz = data.get("quiz_id")
        result = data.get("quiz_result")
        correct_answers = make_lower_register([question.get("correct") for question in quiz.questions])
        user_answers = make_lower_register(result)

        quiz_result = {"final_result": 0, "answers_results": []}
        try:
            for i in range(len(user_answers)):
                if user_answers[i] == correct_answers[i]:
                    quiz_result["final_result"] += 1
                quiz_result["answers_results"].append([user_answers[i], user_answers[i] == correct_answers[i]])
        except [IndexError, TypeError]:
            data.update({"quiz_result": {"error": "некорректный формат ответов"}})
            return

        quiz_result['final_result'] = quiz_result['final_result'] / len(correct_answers) * 100
        data["quiz_result"] = quiz_result
