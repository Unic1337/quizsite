from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from quiz.models import Quiz, QuizResult
from quiz.serializers import QuizSerializer, QuizResultSerializer
from user.models import Profile
from user.serializers import ProfileSerializer


class UserInfoAPI(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        print(serializer.data)
        profile = {"profile": serializer.data}
        user_id = profile["profile"]["id"]

        created_quizzes = []
        for quiz in Quiz.objects.filter(creator_id=user_id):
            created_quizzes.append(QuizSerializer(quiz).data)

        completed_quizzes = []
        for result in QuizResult.objects.filter(user_id=user_id):
            completed_quizzes.append(QuizResultSerializer(result).data)

        profile.update({"created_quizzes": created_quizzes})
        profile.update({"completed_quizzes": completed_quizzes})

        return Response(profile)
