from django.db import models
from django.utils import timezone
from apps.commons.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(BaseModel):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Book(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="genre_books")
    author = models.CharField(max_length=20)
    count = models.IntegerField()
    image = models.FileField(null=True, blank=True, upload_to="books")

    def __str__(self):
        return self.name


class BookApplication(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_applications")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookapplications")
    issue_date = models.DateTimeField(default=timezone.now)
    returned_date = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
