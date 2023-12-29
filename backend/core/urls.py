from django.urls import path

from .views.category_views import category_detail, category_list
from .views.conjugation_views import conjugation_detail, conjugation_list
from .views.example_views import example_detail, example_list
from .views.grammar_views import grammar_detail, grammar_list
from .views.login_views import login_view
from .views.practice_grammar_views import (choice_grammar,
                                           choice_grammar_detail, setence_list)
from .views.profile_views import profile_list
from .views.sentence_views import sentence_detail, sentences_list
from .views.text_translate_views import (text_translate_detail,
                                         text_translate_list)
from .views.text_views import text_detail, text_list
from .views.text_writing_views import text_writing_detail, text_writing_list
from .views.user_views import user_detail, user_list, whoami
from .views.word_views import word_detail, word_list

urlpatterns = [
    path("grammar", grammar_list, name="grammar_list_create"),
    path("grammar/<int:pk>", grammar_detail, name="grammar_detail"),
    path("whoami", whoami, name="whoami"),
    path("user", user_list, name="user_list_create"),
    path("user/<int:pk>", user_detail, name="user_detail"),
    path("profile/<int:user_id>", profile_list, name="profile_list"),
    path("choice_grammar", choice_grammar, name="choice_grammar"),
    path(
        "choice_grammar/<int:pk>", choice_grammar_detail, name="choice_grammar_detail"
    ),
    path("sentence_list", setence_list, name="sentence_list"),
    path("sentences/<int:grammar_id>", sentences_list, name="sentence_list_create"),
    path("sentence/<int:pk>", sentence_detail, name="sentence_detail"),
    path("categories", category_list, name="category_list_create"),
    path("category/<int:pk>", category_detail, name="category_detail"),
    path("words", word_list, name="word_list_create"),
    path("word/<int:pk>", word_detail, name="word_detail"),
    path(
        "conjugation/<int:word_id>", conjugation_list, name="conjugation_list_create"
    ),
    path(
        "conjugation_detail/<int:word_id>/<int:conjugation_id>",
        conjugation_detail,
        name="conjugation_detail",
    ),
    path("example/<int:word_id>", example_list, name="example_list_create"),
    path(
        "example_detail/<int:word_id>/<int:example_id>",
        example_detail,
        name="example_detail",
    ),
    path("text", text_list, name="text_list_create"),
    path("text/<int:text_id>", text_detail, name="text_detail"),
    path(
        "text_translate/<int:text_id>",
        text_translate_list,
        name="text_translate_list_create",
    ),
    path(
        "text_translate_detail/<int:text_id>/<int:text_translate_id>",
        text_translate_detail,
        name="text_translate_detail",
    ),
    path("text_writing", text_writing_list, name="text_writing_list_create"),
    path(
        "text_writing_detail/<int:text_writing_id>",
        text_writing_detail,
        name="text_writing_detail",
    ),
    path("auth/login", login_view, name="login"),
]
