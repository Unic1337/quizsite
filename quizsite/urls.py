from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from quiz.views import *
from quizsite import settings
from user.views import UserInfoAPIRetrieve, FollowAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/quiz/', QuizAPIList.as_view()),
    path('api/quiz/<int:pk>/', QuizAPIRetrieveUpdateDestroy.as_view()),
    path('api/quizresult/', QuizResultAPIList.as_view()),
    path('api/follow/', FollowAPIView.as_view()),
    path('api/auth/users/', UserInfoAPIRetrieve.as_view()),
    path('api/auth/', include('djoser.urls')),
    re_path('api/auth/', include('djoser.urls.authtoken'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
