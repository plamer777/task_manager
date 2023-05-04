"""There ara category goal serialization classes in the file serving to
serialize and deserialize db models"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from core.serializers import UserUpdateRetrieveSerializer
from goals.models import Goal, Category


# -------------------------------------------------------------------------


class GoalSerializer(serializers.ModelSerializer):
    """This serializer works with all views except CreateAPIView for Goal
    models"""

    user = UserUpdateRetrieveSerializer(read_only=True)

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

    def validate_category(self, value: Category) -> Category:
        if value.is_deleted:
            raise serializers.ValidationError(
                _("This action is not allowed for deleted categories")
            )

        return value
