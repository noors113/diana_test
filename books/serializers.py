from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from books.models import Author, Book, Genre, Review

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
        )


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name")


class BookListSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    genres = GenreSerializer(many=True)
    rating = serializers.DecimalField(
        source="avg_rating", max_digits=4, decimal_places=2
    )
    is_in_favorite = serializers.BooleanField(default=False)

    class Meta:
        model = Book
        fields = (
            "id", "title", "authors", "genres", "rating", 'is_in_favorite'
        )


class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = (
            "user",
            "text",
            "rating",
        )


class BookSerializer(BookListSerializer):
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Book
        fields = (
            "title", "authors", "genres", "rating", "description", "reviews")


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, attrs):
        super().validate(attrs)
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords didn't mathc")
        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.create_user(
                username=self.validated_data['email'],
                email=self.validated_data['email'],
                password=self.validated_data['password']
            )

            # Create a token for the user
            token, created = Token.objects.get_or_create(user=user)

            return token
        except IntegrityError:
            raise serializers.ValidationError(
                "User with provided email already exists"
            )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
