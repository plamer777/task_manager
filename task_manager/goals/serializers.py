"""There ara serialization classes in the file serving to serialize and
deserialize db models"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from core.serializers import UserUpdateRetrieveSerializer
from goals.models import Category, Goal, Comment, Status

# -------------------------------------------------------------------------


class CreateCategorySerializer(serializers.ModelSerializer):
    """This serializer works with CreateAPIView for Category models"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CategorySerializer(serializers.ModelSerializer):
    """This serializer works with all views except CreateAPIView for Category
    models"""

    user = UserUpdateRetrieveSerializer()

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = (
            "id",
            "created",
            "updated",
            "user",
        )


class GoalSerializer(serializers.ModelSerializer):
    """This serializer works with all views except CreateAPIView for Goal
    models"""

    user = UserUpdateRetrieveSerializer()

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = (
            "id",
            "created",
            "updated",
            "user",
        )


class GoalCreateSerializer(serializers.ModelSerializer):
    """This serializer works with CreateAPIView for Goal models"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError(
                _("This action is not allowed for deleted categories")
            )
        elif value.user != self.context.get("request").user:
            raise serializers.ValidationError(
                _("Only owner can create a goal in the category")
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """This serializer works with all views except CreateAPIView for Comment
    models"""

    user = UserUpdateRetrieveSerializer()

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = (
            "id",
            "created",
            "updated",
            "goal",
            "user",
        )


class CommentCreateSerializer(serializers.ModelSerializer):
    """This serializer works with CreateAPIView for Comment models"""

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = (
            "id",
            "user",
            "created",
            "updated",
        )

    def validate_goal(self, value):
        if value.status == Status.archived:
            raise serializers.ValidationError(
                _("You cannot leave a comment on a deleted goal")
            )

        elif value.user != self.context.get("request").user:
            raise serializers.ValidationError(
                _("Only owner can leave a comment for this goal")
            )

        return value
