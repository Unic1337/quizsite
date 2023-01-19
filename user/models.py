from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    user_img_url = models.ImageField(null=True, blank=True, upload_to="user_profile_photos/%Y/%m/%d/")
    email = models.EmailField(blank=False, unique=True)

    LOGIN_FIELD = 'email'
