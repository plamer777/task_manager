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


class ModelDateMixin(models.Model):
    """This is an abstract mixin class providing a logic to work with fields
    common for all models"""
    created = models.DateTimeField(
        verbose_name=_("Create date"),
    )

    updated = models.DateTimeField(
        verbose_name=_("Last updated"),
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """This method serves to set up create and update dates"""
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()

        return super().save(*args, **kwargs)


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

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Goal(ModelDateMixin):
    """This class represents a goal model"""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_("Goal category"),
    )

    due_date = models.DateTimeField(
        verbose_name=_("Due date"),
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

    description = models.CharField(
        verbose_name=_("Description"),
        max_length=500,
    )

    class Meta:
        verbose_name = _("Goal")
        verbose_name_plural = _("Goals")


class Comment(models.Model):
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

    text = models.CharField(
        max_length=250,
        verbose_name=_("Text"),

    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

