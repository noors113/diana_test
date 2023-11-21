from django.core.management import BaseCommand

from books.factories import (
    AuthorFactory,
    BookFactory,
    GenreFactory,
    ReviewFactory,
    UserFactory,
)


class Command(BaseCommand):
    help = "Generate test data for the books app"

    def handle(self, *args, **options):
        # Create genres
        genres = GenreFactory.create_batch(5)

        # Create authors
        authors = AuthorFactory.create_batch(5)

        # Create books with genres and authors
        books = BookFactory.create_batch(10)

        for book in books:
            book.genres.set(genres)
            book.authors.set(authors)

        # Create users
        users = UserFactory.create_batch(5)

        # Create reviews
        reviews = ReviewFactory.create_batch(20)

        self.stdout.write(self.style.SUCCESS("Test data successfully generated."))
