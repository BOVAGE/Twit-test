from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (LoginView, RegisterView,
    FollowerView, FollowingView,
    ProfileView)

app_name = "users"
urlpatterns = [
    path('login', LoginView, name="login"),
    path('register', RegisterView, name="register"),
    path('refresh-token', TokenRefreshView.as_view(), name="token-refresh"),
    path('users/<int:id>', ProfileView, name="profile"),
    path('users/<int:id>/followers', FollowerView, name="follower"),
    path('users/<int:id>/followings', FollowingView, name="following"),
]
