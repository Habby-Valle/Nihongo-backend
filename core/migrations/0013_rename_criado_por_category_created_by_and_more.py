# Generated by Django 4.2.3 on 2023-08-08 23:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_category"),
    ]

    operations = [
        migrations.RenameField(
            model_name="category",
            old_name="criado_por",
            new_name="created_by",
        ),
        migrations.AddField(
            model_name="category",
            name="is_created_by_user",
            field=models.BooleanField(default=False),
        ),
    ]
