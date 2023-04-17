"""This file contains classes to configure admin panel"""
from django.contrib import admin
from goals.models import Category, Goal, Comment

# -------------------------------------------------------------------------


class CategoryAdmin(admin.ModelAdmin):
    """This class provides configuration for the category section of the
    admin panel"""

    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")
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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Comment, CommentAdmin)
