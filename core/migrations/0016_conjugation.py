# Generated by Django 4.2.3 on 2023-08-12 21:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0015_category_created_at_category_updated_at_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Conjugation",
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
                ("present", models.CharField(blank=True, max_length=20, null=True)),
                ("negative", models.CharField(blank=True, max_length=20, null=True)),
                ("past", models.CharField(blank=True, max_length=20, null=True)),
                ("te_form", models.CharField(blank=True, max_length=20, null=True)),
                ("volitional", models.CharField(blank=True, max_length=20, null=True)),
                ("potential", models.CharField(blank=True, max_length=20, null=True)),
                ("imperative", models.CharField(blank=True, max_length=20, null=True)),
                ("causative", models.CharField(blank=True, max_length=20, null=True)),
                ("conditional", models.CharField(blank=True, max_length=20, null=True)),
                ("passive", models.CharField(blank=True, max_length=20, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "word",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.word",
                    ),
                ),
            ],
            options={
                "verbose_name": "conjugation",
                "verbose_name_plural": "conjugations",
                "ordering": ("word",),
            },
        ),
    ]
