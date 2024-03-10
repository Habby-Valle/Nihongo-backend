import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

from core.models import *


class GrammarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grammar
        fields = ["grammar", "structure", "level", "explain"]


class GrammarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grammar
        fields = [
            "id",
            "grammar",
            "structure",
            "level",
            "explain",
            "created_by",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"created_by": {"read_only": True}}


class UserCreateSerializer(serializers.ModelSerializer):
    # fonte: https://stackoverflow.com/questions/55906891/django-drf-simple-jwt-authenticationdetail-no-active-account-found-with-the
    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    def validate_first_name(self, value):
        pattern = r"^[a-zA-Z ]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'first_name' deve conter apenas letras"
            )

        return value

    def validate_last_name(self, value):
        pattern = r"^[a-zA-Z ]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'last_name' deve conter apenas letras"
            )

        return value

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "is_active"]


class ProfileSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(read_only=True)
    avatar = serializers.ImageField(required=False)

    def validate_phone(self, value):
        pattern = r"^\d+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'phone' deve conter apenas números"
            )

        return value

    class Meta:
        model = Profile
        fields = ["id", "user", "phone", "date_of_birth", "avatar", "date_created"]


class ProfileUpdateSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=20, required=False)
    date_of_birth = serializers.DateField(required=False, format="%d/%m/%Y")
    avatar = serializers.ImageField(required=False)
    username = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    def validate_phone(self, value):
        pattern = r"^\d+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'phone' deve conter apenas números"
            )

        return value

    def validate_first_name(self, value):
        pattern = r"^[a-zA-ZÀ-ÖØ-öø-ÿ ]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'first_name' deve conter apenas letras"
            )

        if len(value) < 2:
            raise serializers.ValidationError(
                "O campo 'first_name' deve conter pelo menos 2 caracteres"
            )
        return value

    def validate_last_name(self, value):
        pattern = r"^[a-zA-ZÀ-ÖØ-öø-ÿ ]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'last_name' deve conter apenas letras"
            )

        if len(value) < 2:
            raise serializers.ValidationError(
                "O campo 'last_name' deve conter pelo menos 2 caracteres"
            )

        return value

    def validate_username(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "O campo 'username' deve conter pelo menos 5 caracteres"
            )

        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("O campo 'email' é obrigatório")

        return value

    def update(self, instance, validated_data):
        user = instance.user

        user.username = validated_data.get("username", user.username)
        user.email = validated_data.get("email", user.email)
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)

        user.save()

        instance.phone = validated_data.get("phone", instance.phone)
        instance.date_of_birth = validated_data.get(
            "date_of_birth", instance.date_of_birth
        )
        instance.avatar = validated_data.get("avatar", instance.avatar)

        instance.save()

        return instance


class ProfileSerializerResponse(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserSerializer()
    phone = serializers.CharField(max_length=20)
    date_of_birth = serializers.DateField()
    avatar = serializers.ImageField()
    date_created = serializers.DateTimeField()


class PracticeGrammarSerializer(serializers.ModelSerializer):
    grammar = GrammarSerializer(read_only=True)

    class Meta:
        model = PracticeGrammar
        fields = [
            "id",
            "grammar",
            "first_sentence",
            "second_sentence",
            "third_sentence",
            "created_by",
            "created_at",
            "updated_at",
        ]


class SentenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ["id", "sentence", "translate", "annotation", "grammar", "created_by"]


class SentenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = [
            "id",
            "sentence",
            "translate",
            "annotation",
            "grammar",
            "created_by",
            "created_at",
            "updated_at",
        ]


class CategoryCreateSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        pattern = r"^[a-zA-Z ]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'name' deve conter apenas letras"
            )

        return value

    class Meta:
        model = Category
        fields = ["name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "is_created_by_user",
            "created_by",
            "created_at",
            "updated_at",
        ]


class WordCreateSerializer(serializers.ModelSerializer):
    def validate_word(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯+/~]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'word' deve conter apenas letras japonesas."
            )

        return value

    def validate_reading(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯+/~]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'reading' deve conter apenas letras japonesas."
            )

        return value

    class Meta:
        model = Word
        fields = [
            "id",
            "word",
            "reading",
            "meaning",
            "type",
            "level",
            "category",
            "annotation",
        ]


class WordSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    examples_count = serializers.SerializerMethodField()
    class Meta:
        model = Word
        fields = [
            "id",
            "word",
            "reading",
            "meaning",
            "type",
            "level",
            "category",
            "annotation",
            "created_by",
            "created_at",
            "updated_at",
            "examples_count",
        ]

    def get_examples_count(self, obj):
        return obj.Word_Example.count()


class ConjugationCreateSerializer(serializers.ModelSerializer):
    def validate_present(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'present' deve conter apenas letras japonesas."
            )

        return value

    def validate_negative(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'negative' deve conter apenas letras japonesas."
            )

        return value

    def validate_past(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'past' deve conter apenas letras japonesas."
            )

        return value

    def validate_te_form(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'te_form' deve conter apenas letras japonesas."
            )

        return value

    def validate_volitional(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'volitional' deve conter apenas letras japonesas."
            )

        return value

    def validate_passive(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'passive' deve conter apenas letras japonesas."
            )

        return value

    def validate_causative(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'causative' deve conter apenas letras japonesas."
            )

        return value

    def validate_potential(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'potential' deve conter apenas letras japonesas."
            )

        return value

    def validate_imperative(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'imperative' deve conter apenas letras japonesas."
            )

        return value

    def validate_conditional(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'conditional' deve conter apenas letras japonesas."
            )

        return value

    class Meta:
        model = Conjugation
        fields = [
            "word",
            "present",
            "negative",
            "past",
            "te_form",
            "volitional",
            "passive",
            "causative",
            "causative_passive",
            "potential",
            "imperative",
            "conditional",
        ]


class ConjugationSerializer(serializers.ModelSerializer):
    word = WordSerializer(read_only=True)

    class Meta:
        model = Conjugation
        fields = [
            "id",
            "word",
            "present",
            "negative",
            "past",
            "te_form",
            "volitional",
            "passive",
            "causative",
            "causative_passive",
            "potential",
            "imperative",
            "conditional",
            "created_by",
            "created_at",
            "updated_at",
        ]


class ExampleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ["example", "meaning", "annotation"]


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = [
            "id",
            "example",
            "meaning",
            "annotation",
            "word",
            "created_by",
            "created_at",
            "updated_at",
        ]


class TextCreateSerializer(serializers.ModelSerializer):
    def validate_title(self, value):
        pattern = r"^[ぁ-んァ-ン一-龯+/~<>a-zA-Z0-9!@#$%^&*(),.?\":{}|_ ]+$"

        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "O campo 'title' deve conter apenas letras japonesas."
            )

        return value

    class Meta:
        model = Text
        fields = ["title", "text", "translate", "annotation"]


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = [
            "id",
            "title",
            "text",
            "translate",
            "annotation",
            "created_by",
            "created_at",
            "updated_at",
        ]


class TextWritingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextWriting
        fields = ["title", "text", "annotation"]


class TextWritingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextWriting
        fields = [
            "id",
            "title",
            "text",
            "annotation",
            "created_by",
            "created_at",
            "updated_at",
        ]

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=60)
    last_name = serializers.CharField(max_length=60)

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()

    def save(self, request):
        user = super().save(request)
        self.custom_signup(request, user)
        return user
