"""This file contains urls for goal app for the Django project"""
from django.urls import path
from goals import views

# ---------------------------------------------------------------------------

urlpatterns = [
    path("goal_category/create", views.CategoryCreateView.as_view()),
    path("goal_category/list", views.CategoryListView.as_view()),
    path("goal_category/<int:pk>", views.CategoryUpdateRetrieveDeleteView.as_view()),
    path("goal/list", views.GoalListView.as_view()),
    path("goal/create", views.GoalCreateView.as_view()),
    path("goal/<int:pk>", views.GoalUpdateRetrieveDeleteView.as_view()),
    path("goal_comment/list", views.CommentListView.as_view()),
    path("goal_comment/create", views.CommentCreateView.as_view()),
    path("goal_comment/<int:pk>", views.CommentUpdateRetrieveDeleteView.as_view()),
    path("board/create", views.BoardCreateView.as_view()),
    path("board/<int:pk>", views.BoardUpdateRetrieveDeleteView.as_view()),
    path("board/list", views.BoardListView.as_view()),
]
