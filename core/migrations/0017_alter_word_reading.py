# Generated by Django 4.2.3 on 2023-08-12 23:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_conjugation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="word",
            name="reading",
            field=models.CharField(max_length=20),
        ),
    ]
