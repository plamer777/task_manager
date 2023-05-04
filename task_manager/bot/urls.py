"""This file contains urls for telegram bot views"""
from django.urls import path
from bot import views

# -------------------------------------------------------------------------

urlpatterns = [
    path("verify", views.BotConfirmView.as_view()),
]
