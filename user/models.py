from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    user_img_url = models.ImageField(null=True, blank=True, upload_to="user_profile_photos/%Y/%m/%d/")
    email = models.EmailField(blank=True, unique=True)

    LOGIN_FIELD = 'email'


class Follow(models.Model):
    tracking_user = models.ForeignKey(Profile, related_name='tracking_user_article_set', on_delete=models.CASCADE)
    tracked_user = models.ForeignKey(Profile, related_name='tracked_user_article_set', on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)
    is_friends = models.BooleanField(blank=True, null=True)
