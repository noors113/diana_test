# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .factories import AuthorFactory, BookFactory, GenreFactory
from .models import Book, FavoriteBook, Review

User = get_user_model()


class BookViewSetTestCase(APITestCase):
    def setUp(self):
        # Create genres
        self.genres = GenreFactory.create_batch(5)

        # Create authors
        self.authors = AuthorFactory.create_batch(5)

        # Create books with genres and authors
        self.books = BookFactory.create_batch(10)
        self.client = APIClient()

    def test_list_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Book.objects.count())

    def test_retrieve_book(self):
        response = self.client.get(f"/api/books/{self.books[0].pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.books[0].title)

    def test_retrieve_nonexistent_book(self):
        response = self.client.get("/api/books/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class FavoriteBookViewSetTestCase(APITestCase):
    def setUp(self):
        # Create genres
        GenreFactory.create_batch(5)

        # Create authors
        AuthorFactory.create_batch(5)

        # Create books with genres and authors
        BookFactory.create_batch(10)
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@gmail.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_toggle_favorite_book(self):
        book = Book.objects.first()
        response = self.client.post(f"/api/books/{book.pk}/favorite/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            FavoriteBook.objects.filter(user=self.user, book=book).exists())

        response = self.client.post(f"/api/books/{book.pk}/favorite/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            FavoriteBook.objects.filter(user=self.user, book=book).exists()
        )

    def test_toggle_favorite_nonexistent_book(self):
        response = self.client.post("/api/books/999/favorite/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReviewCreateViewTestCase(APITestCase):
    def setUp(self):
        # Create genres
        GenreFactory.create_batch(5)

        # Create authors
        AuthorFactory.create_batch(5)

        # Create books with genres and authors
        BookFactory.create_batch(10)
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="testuser@gmail.com",
            password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_review(self):
        book = Book.objects.first()
        data = {"rating": 4, "text": "Great book!"}
        response = self.client.post(f"/api/books/{book.pk}/reviews/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Review.objects.filter(user=self.user, book=book).exists())

    def test_create_review_without_rating(self):
        book = Book.objects.first()
        data = {"text": "Great book!"}
        response = self.client.post(f"/api/books/{book.pk}/reviews/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_with_invalid_rating(self):
        book = Book.objects.first()
        data = {"rating": 6, "text": "Great book!"}
        response = self.client.post(f"/api/books/{book.pk}/reviews/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_without_text(self):
        book = Book.objects.first()
        data = {"rating": 4}
        response = self.client.post(f"/api/books/{book.pk}/reviews/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_without_authentication(self):
        self.client.logout()
        book = Book.objects.first()
        data = {"rating": 4, "text": "Great book!"}
        response = self.client.post(f"/api/books/{book.pk}/reviews/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SignupViewTests(APITestCase):
    def test_signup_view_with_valid_data(self):
        data = {
            'email': 'testuser@gmail.com',
            'first_name': 'Test',
            'last_name': 'Test',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

        response = self.client.post(reverse("signup"), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get()
        self.assertEqual(user.username, 'testuser@gmail.com')

    def test_signup_view_with_invalid_data(self):
        # Missing password field in the data
        data = {'email': 'testuser'}

        response = self.client.post(reverse("signup"), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_signup_view_email_already_exists(self):
        # Create a user with the same username before making the request
        User.objects.create_user(
            username='existinguser',
            password='testpassword',
            email='existing@gmail.com'
        )

        data = {
            'email': 'existing@gmail.com',
            'first_name': 'Test',
            'last_name': 'Test',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

        response = self.client.post(reverse("signup"), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
