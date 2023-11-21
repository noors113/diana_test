# Create your views here.
from django.contrib.auth import get_user_model
from django.db.models import Avg, Exists, Value, BooleanField, OuterRef
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import BookFilters
from .models import Author, Book, FavoriteBook, Genre
from .serializers import (
    AuthorSerializer,
    BookListSerializer,
    BookSerializer,
    GenreSerializer,
    ReviewSerializer, UserSignupSerializer,
)

User = get_user_model()


class SignupView(CreateAPIView):
    serializer_class = UserSignupSerializer


class BookListCreateView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filterset_class = BookFilters

    def get_queryset(self):
        is_in_favorite = Value(False, output_field=BooleanField())
        if self.request.user.is_authenticated:
            is_in_favorite = Exists(
                queryset=FavoriteBook.objects.filter(
                    user=self.request.user,
                    book_id=OuterRef('id')
                ),
                output_field=BooleanField()
            )
        return Book.objects.prefetch_related("genres", "authors").annotate(
            avg_rating=Avg("reviews__rating"),
            is_in_favorite=is_in_favorite
        )


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.prefetch_related("genres", "authors").annotate(
            avg_rating=Avg("reviews__rating")
        )


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs["book_pk"])
        serializer.save(user=self.request.user, book=book)


class FavoriteBookToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_pk):
        book = get_object_or_404(Book, pk=book_pk)
        favorite, created = FavoriteBook.objects.get_or_create(
            user=request.user, book=book
        )

        if not created:
            favorite.delete()

        return Response(status=status.HTTP_200_OK)
