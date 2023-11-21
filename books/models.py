# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models

from books.managers.user import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(null=True, blank=True, max_length=255)
    email = models.EmailField("Email address", unique=True, )
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    publication_date = models.DateField()
    genres = models.ManyToManyField(Genre)
    authors = models.ManyToManyField(Author)

    pub_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, related_name="reviews",
                             on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class FavoriteBook(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
