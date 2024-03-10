from django.contrib.auth import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Grammar(models.Model):
    nivel_choices = (
        ("N5", "N5"),
        ("N4", "N4"),
        ("N3", "N3"),
        ("N2", "N2"),
        ("N1", "N1"),
        ("UNKNOW", "UNKNOW"),
    )

    grammar = models.CharField(max_length=200)
    structure = models.CharField(max_length=200)
    level = models.CharField(max_length=6, choices=nivel_choices)
    explain = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "grammars"
        ordering = ("id",)

    def __str__(self):
        return f"{self.grammar} - {self.level}"


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone = models.CharField(null=True, blank=True, max_length=15)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(
        default="profile.png", upload_to="uploads", null=True, blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class PracticeGrammar(models.Model):
    grammar = models.ForeignKey(
        Grammar, on_delete=models.SET_NULL, null=True, blank=True
    )
    first_sentence = models.CharField(max_length=250)
    second_sentence = models.CharField(max_length=250)
    third_sentence = models.CharField(max_length=250)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "practice grammar"
        verbose_name_plural = "practice grammars"
        ordering = ("id",)

    def __str__(self):
        return self.grammar.structure


class Sentence(models.Model):
    sentence = models.CharField(max_length=200)
    translate = models.CharField(max_length=200)
    annotation = models.TextField(max_length=300, blank=True, null=True)
    grammar = models.ForeignKey(
        Grammar,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="Grammar_Phrase",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "sentence"
        verbose_name_plural = "sentences"
        ordering = ("translate",)

    def __str__(self):
        return self.sentence


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    is_created_by_user = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Word(models.Model):
    LEVEL_CHOICES = (
        ("N5", "N5"),
        ("N4", "N4"),
        ("N3", "N3"),
        ("N2", "N2"),
        ("N1", "N1"),
        ("Unknown", "Unknown"),
    )

    TYPE_CHOICES = (
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
    )
    word = models.CharField(max_length=20)
    reading = models.CharField(max_length=20)
    meaning = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    level = models.CharField(max_length=8, choices=LEVEL_CHOICES)
    annotation = models.TextField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "word"
        verbose_name_plural = "words"
        ordering = ("word",)

    def __str__(self):
        return f"{self.word} - {self.meaning}"


class Conjugation(models.Model):
    word = models.OneToOneField(Word, on_delete=models.CASCADE, blank=True, null=True)
    present = models.CharField(max_length=20, blank=True, null=True)
    negative = models.CharField(max_length=20, blank=True, null=True)
    past = models.CharField(max_length=20, blank=True, null=True)
    te_form = models.CharField(max_length=20, blank=True, null=True)
    volitional = models.CharField(max_length=20, blank=True, null=True)
    potential = models.CharField(max_length=20, blank=True, null=True)
    imperative = models.CharField(max_length=20, blank=True, null=True)
    causative = models.CharField(max_length=20, blank=True, null=True)
    causative_passive = models.CharField(max_length=20, blank=True, null=True)
    conditional = models.CharField(max_length=20, blank=True, null=True)
    passive = models.CharField(max_length=20, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "conjugation"
        verbose_name_plural = "conjugations"
        ordering = ("word",)

    def __str__(self):
        return self.present


class Example(models.Model):
    example = models.CharField(max_length=200)
    meaning = models.CharField(max_length=200)
    annotation = models.TextField(max_length=500, null=True, blank=True)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, blank=True, null=True, related_name="Word_Example")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "example"
        verbose_name_plural = "examples"
        ordering = ("example",)

    def __str__(self):
        return self.example


class Text(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    translate = models.TextField()
    annotation = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "text"
        verbose_name_plural = "texts"
        ordering = ("title",)

    def __str__(self):
        return self.title


class TextWriting(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    annotation = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = "text-writing"
        verbose_name_plural = "text-writings"
        ordering = ("title",)

    def __str__(self):
        return self.title
