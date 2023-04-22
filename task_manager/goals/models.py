"""This file contains entities such as Category, Goal and Comment"""
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.models import User

# --------------------------------------------------------------------------


class Status(models.IntegerChoices):
    """This class represents available statuses for any Goal model"""

    to_do = 1, _("To do")
    in_progress = 2, _("In progress")
    done = 3, _("Done")
    archived = 4, _("Archived")


class Priority(models.IntegerChoices):
    """This class represents available priorities for Goal models"""

    low = 1, _("Low")
    medium = 2, _("Medium")
    high = 3, _("High")
    critical = 4, _("Critical")


class Roles(models.IntegerChoices):
    """This class represents available roles for Participant models"""
    owner = 1, _("Owner")
    writer = 2, _("Writer")
    reader = 3, _("Reader")


class ModelDateMixin(models.Model):
    """This is an abstract mixin class providing a logic to work with fields
    common for all models"""

    created = models.DateField(
        verbose_name=_("Create date"),
        null=True,
        blank=True,
    )

    updated = models.DateField(
        verbose_name=_("Last updated"),
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """This method serves to set up create and update dates"""
        if not self.id:
            self.created = timezone.now().date()
        self.updated = timezone.now().date()

        return super().save(*args, **kwargs)


class Board(ModelDateMixin):
    """This class represents a board model"""
    title = models.CharField(
        max_length=50,
        verbose_name=_("Title"),
    )

    is_deleted = models.BooleanField(
        verbose_name=_('Is deleted'),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Board")
        verbose_name_plural = _("Boards")

    def __str__(self):
        return self.title


class Participant(ModelDateMixin):
    """This class represents a participant model"""
    role = models.SmallIntegerField(
        choices=Roles.choices,
        verbose_name=_("Role"),
        default=Roles.owner,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("User"),
        related_name='participants',
    )

    board = models.ForeignKey(
        Board,
        on_delete=models.PROTECT,
        verbose_name=_("Board"),
        related_name='participants',
    )

    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        unique_together = ('board', 'user')

    def __str__(self):
        return self.role


class Category(ModelDateMixin):
    """This class represents a category model"""

    title = models.CharField(
        max_length=50,
        verbose_name=_("Category")
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Author"),
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_("Deleted")
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.PROTECT,
        verbose_name=_("Board"),
        related_name='categories',
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title


class Goal(ModelDateMixin):
    """This class represents a goal model"""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_("Goal category"),
    )

    due_date = models.DateField(
        verbose_name=_("Due date"),
        null=True,
        blank=True,
    )

    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        verbose_name=_("Status"),
        default=Status.to_do,
    )

    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices,
        verbose_name=_("Priority"),
        default=Priority.medium,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Author"),
    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=50,
    )

    description = models.TextField(
        verbose_name=_("Description"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Goal")
        verbose_name_plural = _("Goals")

    def __str__(self):
        return self.title


class Comment(ModelDateMixin):
    """This class represents a comment model"""

    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        verbose_name=_("Goal"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Author"),
    )

    text = models.TextField(
        verbose_name=_("Text"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.text
