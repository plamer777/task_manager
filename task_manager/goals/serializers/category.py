"""There ara category serialization classes in the file serving to serialize and
deserialize db models"""
from rest_framework import serializers
from core.serializers import UserUpdateRetrieveSerializer
from goals.models import Category, Board

# -------------------------------------------------------------------------


class CreateCategorySerializer(serializers.ModelSerializer):
    """This serializer works with CreateAPIView for Category models"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    board = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all(),
    )

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class CategorySerializer(serializers.ModelSerializer):
    """This serializer works with all views except CreateAPIView for Category
    models"""

    user = UserUpdateRetrieveSerializer(read_only=True)
    board = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = (
            "id",
            "created",
            "updated",
            "user",
        )
