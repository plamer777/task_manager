"""This unit contains User model inherited from AbstractUser"""
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# -------------------------------------------------------------------------


class User(AbstractUser):
    """User model serves to work with users"""

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(10), MaxValueValidator(100)],
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username
