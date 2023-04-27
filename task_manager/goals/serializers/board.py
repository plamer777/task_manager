"""There ara participant and board serialization classes in the file serving to
serialize and deserialize db models"""
from django.db import transaction
from rest_framework import serializers
from core.models import User
from goals.models import Board, Participant, Roles

# ------------------------------------------------------------------------


class ParticipantSerializer(serializers.ModelSerializer):
    """The ParticipantSerializer class serves to serialize and deserialize
    participant models"""

    role = serializers.ChoiceField(required=True, choices=Participant.editable_roles)

    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    board = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = Participant
        fields = "__all__"
        real_only_fields = (
            "id",
            "created",
            "updated",
            "board",
        )


class BoardCreateSerializer(serializers.ModelSerializer):
    """The BoardCreateSerializer class serves to create a new board"""

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = (
            "id",
            "created",
            "updated",
        )

    def create(self, validated_data) -> Board:
        user = self.context.get("request").user
        with transaction.atomic():
            board = Board.objects.create(**validated_data)
            board.is_deleted = False
            board.save()
            Participant.objects.create(
                board=board,
                user=user,
            )
        return board


class BoardSerializer(serializers.ModelSerializer):
    """The BoardSerializer class serves to retrieve, update or delete a
    single board"""

    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = (
            "id",
            "created",
            "updated",
        )

    def update(self, instance: Board, validated_data) -> Board:
        user = self.context.get("request").user
        new_participants = {
            participant["user"].id: participant
            for participant in validated_data.pop("participants")
            if participant["user"] != user
        }

        old_participants = instance.participants.exclude(user=user)

        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user.id not in new_participants:
                    old_participant.delete()

                else:
                    new_role = new_participants[old_participant.user.id]["role"]
                    if old_participant.role != new_role:
                        old_participant.role = new_role
                        old_participant.save()
                    del new_participants[old_participant.user.id]

            [
                Participant.objects.create(board=instance, **data)
                for data in new_participants.values()
            ]
            instance.title = validated_data.get("title")
            instance.save()

        return instance


class BoardListSerializer(serializers.ModelSerializer):
    """The BoardListSerializer class serves to get a list of boards"""

    class Meta:
        model = Board
        fields = "__all__"
