# Generated by Django 4.2.3 on 2023-08-03 13:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_alter_sentence_options"),
    ]

    operations = [
        migrations.RenameField(
            model_name="practicegrammar",
            old_name="first_setence",
            new_name="first_sentence",
        ),
    ]
