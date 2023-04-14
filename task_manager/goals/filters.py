"""The file contains a GoalListFilter class to provide filtering for CBVs
working with the Goal model"""
from django.db import models
from django_filters import IsoDateTimeFilter
from django_filters.rest_framework import FilterSet
from goals.models import Goal

# --------------------------------------------------------------------------


class GoalListFilter(FilterSet):
    """The GoalListFilter class provides a way to filter the list of goals.
    It allows you to filter entities by the due date, priority, status and
    category"""
    filter_overrides = {
        models.DateTimeField: {'filter_class': IsoDateTimeFilter}
    }

    class Meta:
        model = Goal
        fields = {
            'due_date': ('lte', 'gte'),
            'priority': ('exact', 'in'),
            'status': ('exact', 'in'),
            'category': ('exact', 'in'),
        }
