# Generated by Django 4.2.3 on 2024-04-13 18:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0027_alter_example_word"),
    ]

    operations = [
        migrations.AlterField(
            model_name="word",
            name="level",
            field=models.CharField(
                blank=True,
                choices=[
                    ("N5", "N5"),
                    ("N4", "N4"),
                    ("N3", "N3"),
                    ("N2", "N2"),
                    ("N1", "N1"),
                    ("Unknown", "Unknown"),
                ],
                max_length=8,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="word",
            name="reading",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="word",
            name="type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Verb - Group 1", "Verb - Group 1 "),
                    ("Verb - Group 2", "Verb - Group 2"),
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
                null=True,
            ),
        ),
    ]
