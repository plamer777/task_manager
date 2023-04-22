"""This file contains permission classes to manage user access to data"""
from rest_framework import permissions
from goals.models import Participant, Roles, Category, Goal, Comment

# -------------------------------------------------------------------------


class BoardPermission(permissions.BasePermission):
    """The BoardPermission class serves to restrict access to board for users
    who absent in the participant list"""

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return Participant.objects.filter(
                user=request.user, board=obj).exists()
        else:
            return Participant.objects.filter(
                user=request.user, board=obj, role=Roles.owner
            ).exists()


class CategoryPermission(permissions.BasePermission):
    """The CategoryPermission class serves to restrict access to category for
    users who are not a participant of the category's board"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (
                Category.objects.select_related("board")
                .filter(board__participants__user=request.user, board=obj.board)
                .exists()
            )
        else:
            return (
                Category.objects.select_related("board")
                .filter(
                    board__participants__user=request.user,
                    board=obj.board,
                    board__participants__role__in=[Roles.owner, Roles.writer],
                )
                .exists()
            )


class CategoryCreatePermission(permissions.BasePermission):
    """The CategoryCreatePermission class serves to restrict
    creation of a category for users who are not a participant of the
    category's board"""

    def has_permission(self, request, view):
        board = request.data.get("board")
        return Participant.objects.filter(
            user=request.user, board=board, role__in=[Roles.owner, Roles.writer]
        ).exists()


class GoalCreatePermission(permissions.BasePermission):
    """The GoalCreatePermission class serves to prevent the creation of a new
    goal for users who are not members of the board"""

    def has_permission(self, request, view):
        category_id = request.data.get("category")
        category = Category.objects.get(id=category_id)
        return Participant.objects.filter(
            user=request.user,
            board=category.board,
            role__in=[Roles.owner, Roles.writer],
        ).exists()


class GoalPermission(permissions.BasePermission):
    """The GoalPermission class serves to prevent access to
    a goal for users who are not members of the board"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (
                Goal.objects.select_related("category")
                .filter(
                    category__board__participants__user=request.user,
                    category__board=obj.category.board,
                )
                .exists()
            )
        else:
            return (
                Goal.objects.select_related("category")
                .filter(
                    category__board__participants__user=request.user,
                    category__board=obj.category.board,
                    category__board__participants__role__in=[Roles.owner, Roles.writer],
                )
                .exists()
            )


class CommentCreatePermission(permissions.BasePermission):
    """The CommentCreatePermission class serves to prevent the creation of
    a new comment for users who are not members of the board"""

    def has_permission(self, request, view):
        goal_id = request.data.get("goal")
        goal = Goal.objects.get(id=goal_id)
        return (
            Participant.objects.select_related("user")
            .filter(
                user=request.user,
                board=goal.category.board,
                role__in=[Roles.owner, Roles.writer],
            )
            .exists()
        )


class CommentPermission(permissions.BasePermission):
    """The CommentPermission class serves to prevent the access to comments
    for users who are not members of the board"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (
                Comment.objects.select_related("goal")
                .filter(
                    goal__category__board__participants__user=request.user,
                    goal__category__board=obj.goal.category.board,
                )
                .exists()
            )
        else:
            return (
                Comment.objects.select_related("goal")
                .filter(
                    goal__category__board__participants__user=request.user,
                    goal__category__board=obj.goal.category.board,
                    user=request.user,
                    goal__category__board__participants__role__in=[
                        Roles.owner,
                        Roles.writer,
                    ],
                )
                .exists()
            )
