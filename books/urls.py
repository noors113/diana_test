# books/urls.py
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from .views import (
    AuthorListView,
    BookDetailView,
    BookListCreateView,
    FavoriteBookToggleView,
    GenreListView,
    ReviewCreateView, SignupView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", ObtainAuthToken.as_view(), name="signin"),
    path("books/", BookListCreateView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("genres/", GenreListView.as_view(), name="genre-list"),
    path("authors/", AuthorListView.as_view(), name="author-list"),
    path(
        "books/<int:book_pk>/reviews/", ReviewCreateView.as_view(),
        name="review-create"
    ),
    path(
        "books/<int:book_pk>/favorite/",
        FavoriteBookToggleView.as_view(),
        name="favorite-book-toggle",
    ),
]
