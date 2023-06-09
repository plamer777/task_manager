# Generated by Django 4.1.7 on 2023-04-17 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateField(blank=True, null=True, verbose_name="Create date"),
                ),
                (
                    "updated",
                    models.DateField(
                        blank=True, null=True, verbose_name="Last updated"
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="Category")),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="Deleted"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Goal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateField(blank=True, null=True, verbose_name="Create date"),
                ),
                (
                    "updated",
                    models.DateField(
                        blank=True, null=True, verbose_name="Last updated"
                    ),
                ),
                (
                    "due_date",
                    models.DateField(blank=True, null=True, verbose_name="Due date"),
                ),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "To do"),
                            (2, "In progress"),
                            (3, "Done"),
                            (4, "Archived"),
                        ],
                        default=1,
                        verbose_name="Status",
                    ),
                ),
                (
                    "priority",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "Low"),
                            (2, "Medium"),
                            (3, "High"),
                            (4, "Critical"),
                        ],
                        default=2,
                        verbose_name="Priority",
                    ),
                ),
                ("title", models.CharField(max_length=50, verbose_name="Title")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="goals.category",
                        verbose_name="Goal category",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
            ],
            options={
                "verbose_name": "Goal",
                "verbose_name_plural": "Goals",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateField(blank=True, null=True, verbose_name="Create date"),
                ),
                (
                    "updated",
                    models.DateField(
                        blank=True, null=True, verbose_name="Last updated"
                    ),
                ),
                ("text", models.TextField(blank=True, null=True, verbose_name="Text")),
                (
                    "goal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="goals.goal",
                        verbose_name="Goal",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Author",
                    ),
                ),
            ],
            options={
                "verbose_name": "Comment",
                "verbose_name_plural": "Comments",
            },
        ),
    ]
