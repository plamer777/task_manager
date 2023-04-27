"""This file contains classes to configure admin panel"""
from django.contrib import admin
from goals.models import Category, Goal, Comment, Board, Participant

# -------------------------------------------------------------------------


class CategoryAdmin(admin.ModelAdmin):
    """This class provides configuration for the category section of the
    admin panel"""

    list_display = ("title", "board", "created", "updated")
    search_fields = ("title", "board")
    readonly_fields = ("created", "updated")


class GoalAdmin(admin.ModelAdmin):
    """This class provides configuration for the goal section of the
    admin panel"""

    list_display = ("title", "description", "created", "updated")
    search_fields = ("title", "description")
    list_filter = ("due_date", "user", "category")
    readonly_fields = ("created", "updated")


class CommentAdmin(admin.ModelAdmin):
    """This class provides configuration for the comment section of the
    admin panel"""

    list_display = ("text", "user", "created", "updated")
    search_fields = ("user", "created")
    list_filter = ("user", "goal")
    readonly_fields = ("created", "updated")


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("user", "board", "created", "updated")
    search_fields = ("user", "board")
    list_filter = ("user", "board")
    readonly_fields = ("created", "updated")


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "is_deleted", "created", "updated")
    search_fields = ("title",)
    list_filter = ("is_deleted",)
    readonly_fields = ("created", "updated")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Comment, CommentAdmin)
