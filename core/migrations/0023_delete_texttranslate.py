# Generated by Django 4.2.3 on 2024-01-01 15:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0022_text_translate_alter_word_type"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TextTranslate",
        ),
    ]
