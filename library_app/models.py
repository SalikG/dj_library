from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.title} - {self.author} - {self.genre}"


class Magazine(models.Model):
    title = models.CharField(max_length=200)
    genre = models.ForeignKey(Genre, models.PROTECT)

    def __str__(self):
        return f"{self.title} - {self.genre}"


class BookLoan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    due_date = models.DateTimeField()
    issued_date = models.DateTimeField(auto_now=True)
    hand_in_date = models.DateTimeField(null=True)
    is_handed_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book} - {self.user} - {self.is_handed_in}"


class MagazineLoan(models.Model):
    magazine = models.ForeignKey(Magazine, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    due_date = models.DateTimeField()
    issued_date = models.DateTimeField(auto_now=True)
    hand_in_date = models.DateTimeField(null=True)
    is_handed_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.magazine} - {self.user} - {self.is_handed_in}"






