from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers

from quiz.views import *
from quizsite import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/quiz/', QuizAPIList.as_view()),
    path('api/quiz/<int:pk>/', QuizAPIUpdate.as_view()),
    path('api/quizdelete/<int:pk>/', QuizAPIDestroy.as_view()),
    path('api/auth/', include('djoser.urls')),
    re_path('api/auth/', include('djoser.urls.authtoken'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)