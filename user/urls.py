from django.urls import path

from user.views import UserInfoAPIRetrieve, FollowAPIView

urlpatterns = [
    path('follow/', FollowAPIView.as_view()),
    path('auth/users/<int:pk>/', UserInfoAPIRetrieve.as_view(), name="get_update_profile"),
]
