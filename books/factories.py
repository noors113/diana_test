from factory import Faker, SubFactory, Sequence
from factory.django import DjangoModelFactory

from books.models import Author, Book, Genre, Review, CustomUser


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book

    title = Faker("sentence")
    description = Faker("paragraph")
    publication_date = Faker("date_this_decade")


class GenreFactory(DjangoModelFactory):
    class Meta:
        model = Genre

    name = Sequence(lambda x: f"Genre {x}")


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    name = Faker("name")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = Faker("user_name")
    email = Faker("email")
    password = Faker("password")


class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    book = SubFactory(BookFactory)
    user = SubFactory(UserFactory)
    rating = Faker("random_int", min=1, max=5)
    text = Faker("paragraph")
