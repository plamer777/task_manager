"""This file contains CBVs for goals app"""
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from goals.filters import GoalListFilter
from goals.models import Category, Goal, Comment, Status
from goals.serializers import (
    CreateCategorySerializer,
    CategorySerializer,
    GoalSerializer,
    GoalCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)

# -------------------------------------------------------------------------


class CategoryCreateView(CreateAPIView):
    """This view is used to create a category"""

    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCategorySerializer


class CategoryListView(ListAPIView):
    """The CategoryListView provides logic to display a list of categories"""

    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, is_deleted=False)


class CategoryUpdateRetrieveDeleteView(RetrieveUpdateDestroyAPIView):
    """This view is used to show, update and delete a single category"""

    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=["is_deleted"])
            instance.goal_set.update(status=Status.archived)
        return instance


class GoalListView(ListAPIView):
    """The GoalListView provides logic to display a list of goals"""

    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_class = GoalListFilter
    ordering_fields = ["-priority", "due_date"]
    ordering = ["priority"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user,
            status__lt=Status.archived,
        )


class GoalCreateView(CreateAPIView):
    """This view is used to create a goal"""

    queryset = Goal.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalUpdateRetrieveDeleteView(RetrieveUpdateDestroyAPIView):
    """This view is used to show, update and delete a single goal"""

    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(
            user=self.request.user,
            status__lt=Status.archived,
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.status = Status.archived
            instance.save(update_fields=["status"])
            instance.comment_set.delete()
        return instance


class CommentListView(ListAPIView):
    """The CommentListView provides logic to display a list of comments"""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (OrderingFilter,)
    ordering_fields = ["created", "updated"]
    ordering = ["-created"]

    def get_queryset(self):
        return Comment.objects.filter(
            goal=self.request.GET.get("goal"),
            user=self.request.user,
            goal__status__lt=Status.archived,
        )


class CommentCreateView(CreateAPIView):
    """This view is used to create a comment"""

    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer


class CommentUpdateRetrieveDeleteView(RetrieveUpdateDestroyAPIView):
    """This view is used to show, update and delete a single comment"""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(
            user=self.request.user,
            goal__status__lt=Status.archived,
        )
