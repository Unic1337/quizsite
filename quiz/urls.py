from django.urls import path
from quiz.views import *

urlpatterns = [
    path('quiz/', QuizAPIList.as_view(), name='get_quizzes'),
    path('quiz/<int:pk>/', QuizAPIRetrieveUpdateDestroy.as_view()),
    path('quizresult/', QuizResultAPIList.as_view()),
]
