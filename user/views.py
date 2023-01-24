from rest_framework import status
from rest_framework.permissions import *
from rest_framework.generics import RetrieveUpdateAPIView, GenericAPIView, DestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.settings import api_settings

from quiz.permissions import IsProfileOwner
from quizsite.settings import DOMAIN
from quiz.models import Quiz, QuizResult
from quiz.serializers import QuizSerializer, QuizResultSerializer
from user.models import Profile, Follow
from user.serializers import ProfileSerializer, FollowSerializer


class UserInfoAPIRetrieve(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsProfileOwner, )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        profile = {"profile": serializer.data}
        user_id = profile["profile"]["id"]

        created_quizzes = []
        for quiz in Quiz.objects.filter(creator_id=user_id):
            quiz = QuizSerializer(quiz).data
            if quiz["quiz_img_url"]:
                quiz["quiz_img_url"] = DOMAIN + quiz["quiz_img_url"]
            created_quizzes.append(quiz)

        completed_quizzes = []
        for result in QuizResult.objects.filter(user_id=user_id):
            result = QuizResultSerializer(result).data
            quiz = Quiz.objects.get(pk=result.get('quiz_id'))
            result.update({'quiz_name': QuizSerializer(quiz).data['title']})
            completed_quizzes.append(result)

        following = []
        followers = []
        friends = []
        for follow in Follow.objects.filter(user_is_following=user_id):
            user_is_being_followed = Profile.objects.get(pk=follow.user_is_being_followed.id)
            if follow.is_friends:
                friends.append(ProfileSerializer(user_is_being_followed).data)
            else:
                following.append(ProfileSerializer(user_is_being_followed).data)

        for follow in Follow.objects.filter(user_is_being_followed=user_id):
            user_is_following = Profile.objects.get(pk=follow.user_is_following.id)
            if not follow.is_friends:
                followers.append(ProfileSerializer(user_is_following).data)

        profile.update({"created_quizzes": created_quizzes})
        profile.update({"completed_quizzes": completed_quizzes})
        profile.update({"following": following})
        profile.update({"followers": followers})
        profile.update({"friends": friends})

        return Response(profile)


class FollowAPIView(CreateAPIView, DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.create_relation(serializer.validated_data, request._user)
        if instance.get('error', False):
            headers = self.get_success_headers(serializer.validated_data)
            return Response(instance, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_is_following = request._user.id
        user_is_being_followed = serializer.data['user_is_being_followed']
        instance = Follow.objects.get(user_is_following=user_is_following, user_is_being_followed_id=user_is_being_followed)

        if Follow.objects.filter(user_is_following=user_is_being_followed, user_is_being_followed_id=user_is_following).exists():
            friend = Follow.objects.get(user_is_following=user_is_being_followed, user_is_being_followed_id=user_is_following)
            self.update(friend, is_friends=False)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def create_relation(self, data, user_is_following):
        user_is_being_followed = data['user_is_being_followed']
        data['user_is_following'] = user_is_following

        if Follow.objects.filter(user_is_following=user_is_following.id, user_is_being_followed=user_is_being_followed.id).exists():
            data = {'error': 'already following'}
            return data

        if user_is_following == user_is_being_followed:
            data = {'error': 'cant follow yourself'}
            return data

        if Follow.objects.filter(user_is_being_followed=user_is_following.id, user_is_following=user_is_being_followed.id).exists():
            data.update({'is_friends': True})
            friend = Follow.objects.get(user_is_being_followed=user_is_following.id, user_is_following=user_is_being_followed.id)
            self.update(friend, is_friends=True)

        return data

    def update(self, data, *args, **kwargs):
        instance = data
        serializer = self.get_serializer(instance, data=kwargs, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
