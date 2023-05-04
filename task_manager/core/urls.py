"""This file contains urls for core app"""
from django.urls import path
from core import views

# -----------------------------------------------------------------------

urlpatterns = [
    path("login", views.UserLoginView.as_view()),
    path("signup", views.UserRegistrationView.as_view()),
    path("profile", views.UserUpdateRetrieveView.as_view()),
    path("update_password", views.UserUpdatePasswordView.as_view()),
]
