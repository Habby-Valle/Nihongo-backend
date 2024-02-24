# Generated by Django 4.2.3 on 2024-02-10 13:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0025_conjugation_causative_passive"),
    ]

    operations = [
        migrations.AddField(
            model_name="word",
            name="annotation",
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="word",
            name="type",
            field=models.CharField(
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
            ),
        ),
    ]