from django.contrib.auth.models import User
from django.db import models
from user.models import Profile


class Quiz(models.Model):
    title = models.CharField(max_length=60)
    quiz_img_url = models.ImageField(null=True, blank=True, upload_to="quiz_photos/%Y/%m/%d/")
    questions = models.JSONField()
    creation_time = models.DateTimeField(auto_now_add=True)
    change_time = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['id']


class QuizResult(models.Model):
    user_id = models.ForeignKey(Profile, null=True, on_delete=models.CASCADE)
    quiz_id = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_result = models.JSONField()
    creation_time = models.DateTimeField(auto_now_add=True)
