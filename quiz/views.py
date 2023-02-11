from rest_framework import status, generics
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.settings import api_settings

from quiz.models import Quiz, QuizResult
from quiz.permissions import IsOwnerOrReadOnly
from quiz.serializers import QuizSerializer, QuizResultSerializer
from user.models import Profile
from user.serializers import ProfileSerializer


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
<<<<<<< HEAD
        for result in instance.quizresult_set.all().select_related("user_id"):
            username = result.user_id.username
            result = QuizResultSerializer(result).data
            result.update({"username": username})
=======
        for result in request._user.quizresult_set.all():
            user = result.user_id
            result = QuizResultSerializer(result).data
            result.update({"username": user.username})
>>>>>>> f878692612f0864d305775c963d16d14f3e04169
            quiz["quiz_results"].append(result)

        return Response(quiz)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class QuizResultAPIList(generics.ListCreateAPIView):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.create_result(serializer.validated_data)

        if not request._user.id:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data["quiz_result"], status=status.HTTP_200_OK, headers=headers)

        serializer.validated_data.update({"user_id": request._user})
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

    def make_lower_register(self, arr):
        if isinstance(arr, list):
            return [i.lower() if not isinstance(i, list) else [j.lower() for j in i] for i in arr]
        return arr

    def create_result(self, data):
        quiz = data["quiz_id"]
        result = data.get("quiz_result")
        correct_answers = [question.get("correct") for question in quiz.questions]
        correct_answers = self.make_lower_register(correct_answers)
        user_answers = self.make_lower_register(result)

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
