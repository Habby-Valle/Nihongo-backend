# Generated by Django 4.2.3 on 2024-01-03 18:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0023_delete_texttranslate"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="example",
            name="reading",
        ),
    ]
