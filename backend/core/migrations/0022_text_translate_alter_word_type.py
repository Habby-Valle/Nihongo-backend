# Generated by Django 4.2.3 on 2023-12-26 20:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0021_alter_word_level_alter_word_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="text",
            name="translate",
            field=models.TextField(
                default=datetime.datetime(2023, 12, 26, 20, 9, 21, 140162)
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="word",
            name="type",
            field=models.CharField(
                choices=[
                    ("Verb - Group 1", "Verb - Group 1 "),
                    ("Verb - Group 2 ", "Verb - Group 2"),
                    ("Verb - Group 3", "Verb - Group 3"),
                    ("Adjective - i", "Adjective - i"),
                    ("Adjective - na", "Adjective - na"),
                    ("Noun", "Noun"),
                    ("Adverb", "Adverb"),
                    ("Pronoun", "Pronoun"),
                    ("Preposition", "Preposition"),
                    ("Conjunction", "Conjunction"),
                    ("Interjection", "Interjection"),
                    ("Phrase", "Phrase"),
                    ("Expression", "Expression"),
                    ("Counter", "Counter"),
                    ("Number", "Number"),
                    ("Prefix", "Prefix"),
                    ("Suffix", "Suffix"),
                    ("Particle", "Particle"),
                    ("Auxiliary verb", "Auxiliary verb"),
                    ("Honorific", "Honorific"),
                    ("Onomatopoeia", "Onomatopoeia"),
                    ("Proverb", "Proverb"),
                    ("Other", "Other"),
                    ("Unknow", "Unknow"),
                ],
                max_length=20,
            ),
        ),
    ]
