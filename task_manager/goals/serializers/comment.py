"""There ara comment serialization classes in the file serving to serialize and
deserialize db models"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from core.serializers import UserUpdateRetrieveSerializer
from goals.models import Comment, Status, Goal


# -------------------------------------------------------------------------


class CommentSerializer(serializers.ModelSerializer):
    """This serializer works with all views except CreateAPIView for Comment
    models"""

    user = UserUpdateRetrieveSerializer(read_only=True)

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

    def validate_goal(self, value: Goal) -> Goal:
        if value.status == Status.archived:
            raise serializers.ValidationError(
                _("You cannot leave a comment on a deleted goal")
            )

        return value
