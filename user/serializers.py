from rest_framework import serializers

from user.models import Profile, Follow


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "username", "user_img_url", "last_login", "date_joined",)


class FollowSerializer(serializers.ModelSerializer):
    user_is_following = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = ("user_is_being_followed", "user_is_following",)
