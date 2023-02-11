from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from quizsite import settings
<<<<<<< HEAD


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('quiz.urls')),
    path('api/', include('user.urls')),
=======
from user.views import UserInfoAPIRetrieve, FollowAPIView

# quiz_router = routers.SimpleRouter()
# quiz_router.register(r'quiz', )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/quiz/', QuizAPIList.as_view()),
    path('api/quiz/<int:pk>/', QuizAPIRetrieveUpdateDestroy.as_view()),
    path('api/quizresult/', QuizResultAPIList.as_view()),
    path('api/follow/', FollowAPIView.as_view()),
    path('api/auth/users/<int:pk>/', UserInfoAPIRetrieve.as_view()),
>>>>>>> f878692612f0864d305775c963d16d14f3e04169
    path('api/auth/', include('djoser.urls')),
    re_path('api/auth/', include('djoser.urls.authtoken')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
