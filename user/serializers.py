from rest_framework import serializers

from user.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'username', 'user_img_url', "last_login", 'date_joined')

    LOGIN_FIELD = 'email'
