# Generated by Django 4.2.3 on 2023-08-03 11:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_rename_setence_sentence_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="sentence",
            options={
                "ordering": ("translate",),
                "verbose_name": "sentence",
                "verbose_name_plural": "sentences",
            },
        ),
    ]