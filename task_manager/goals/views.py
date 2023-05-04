"""This file contains CBVs for goals app"""
from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from goals.filters import GoalListFilter
from goals.models import Category, Goal, Comment, Status, Board
from goals import serializers
from goals.permissions import (
    BoardPermission,
    CategoryPermission,
    CategoryCreatePermission,
    GoalPermission,
    GoalCreatePermission,
    CommentCreatePermission,
    CommentPermission,
)

# -------------------------------------------------------------------------


class CategoryCreateView(CreateAPIView):
    """This view is used to create a category"""

    permission_classes = [IsAuthenticated, CategoryCreatePermission]
    serializer_class = serializers.CreateCategorySerializer

    def get_queryset(self):
        return Category.objects.select_related("board").filter(
            board=self.request.data.get("board")
        )


class CategoryListView(ListAPIView):
    """The CategoryListView provides logic to display a list of categories"""

    permission_classes = [IsAuthenticated, CategoryPermission]
    serializer_class = serializers.CategorySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    ordering_fields = ["title", "created"]
    filterset_fields = ["board"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Category.objects.select_related("board").filter(
            board__participants__user=self.request.user,
            is_deleted=False,
        )


class CategoryUpdateRetrieveDeleteView(RetrieveUpdateDestroyAPIView):
    """This view is used to show, update and delete a single category"""

    permission_classes = [IsAuthenticated, CategoryPermission]
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        return Category.objects.select_related("board").filter(
            board__participants__user=self.request.user,
            is_deleted=False,
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=["is_deleted"])
            instance.goal_set.update(status=Status.archived)
        return instance


class GoalListView(ListAPIView):
    """The GoalListView provides logic to display a list of goals"""

    serializer_class = serializers.GoalSerializer
    permission_classes = [IsAuthenticated, GoalPermission]
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = GoalListFilter
    ordering_fields = ["-priority", "due_date"]
    ordering = ["priority"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        Goal.objects.filter(due_date__lt=timezone.now().date()).update(
            status=Status.archived
        )

        goals = Goal.objects.select_related("category").filter(
            category__board__participants__user=self.request.user,
            status__lt=Status.archived,
        )
        return goals


class GoalCreateView(CreateAPIView):
    """This view is used to create a goal"""

    permission_classes = [IsAuthenticated, GoalCreatePermission]
    serializer_class = serializers.GoalCreateSerializer

    def get_queryset(self):
        return Goal.objects.select_related("category").filter(
            category=self.request.data.get("category"),
            category__board__participants__user=self.request.user,
            category__is_deleted=False,
        )


class GoalUpdateRetrieveDeleteView(RetrieveUpdateDestroyAPIView):
    """This view is used to show, update and delete a single goal"""

    serializer_class = serializers.GoalSerializer
    permission_classes = [IsAuthenticated, GoalPermission]

    def get_queryset(self):
        return Goal.objects.select_related("category").filter(
            category__board__participants__user=self.request.user,
            status__lt=Status.archived,
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.status = Status.archived
            instance.save(update_fields=["status"])
            instance.comment_set.all().delete()
        return instance


class CommentListView(ListAPIView):
    """The CommentListView provides logic to display a list of comments"""

    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated, CommentPermission]
    filter_backends = (OrderingFilter,)
    ordering_fields = ["created", "updated"]
    ordering = ["-created"]

    def get_queryset(self):
        return Comment.objects.select_related("goal").filter(
            goal=self.request.GET.get("goal"),
            goal__category__board__participants__user=self.request.user,
            goal__status__lt=Status.archived,
        )


class CommentCreateView(CreateAPIView):
    """This view is used to create a comment"""

    permission_classes = [IsAuthenticated, CommentCreatePermission]
    serializer_class = serializers.CommentCreateSerializer

    def get_queryset(self):
        return Comment.objects.select_related("goal").filter(
            goal__category__board__participants__user=self.request.user,
            goal__status__lt=Status.archived,
        )


class CommentUpdateRetrieveDeleteView(RetrieveUpdateDestroyAPIView):
    """This view is used to show, update and delete a single comment"""

    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated, CommentPermission]

    def get_queryset(self):
        return Comment.objects.select_related("goal").filter(
            goal__category__board__participants__user=self.request.user,
            goal__status__lt=Status.archived,
        )


class BoardCreateView(CreateAPIView):
    """This view is used to create a new board"""

    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.BoardCreateSerializer


class BoardListView(ListAPIView):
    """The BoardListView provides logic to display a list of all available
    boards"""

    serializer_class = serializers.BoardListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["title"]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(
            participants__user=self.request.user, is_deleted=False
        )


class BoardUpdateRetrieveDeleteView(RetrieveUpdateDestroyAPIView):
    """This view is used to show, update and delete a single board"""

    serializer_class = serializers.BoardSerializer
    permission_classes = [IsAuthenticated, BoardPermission]

    def get_queryset(self):
        return Board.objects.filter(
            is_deleted=False,
        )

    def perform_destroy(self, instance: Board) -> Board:
        with transaction.atomic():
            instance.is_deleted = True
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Status.archived)

            instance.save()

        return instance
