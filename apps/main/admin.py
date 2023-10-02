from django.contrib import admin
from .models import Book, Genre, BookApplication

# Register your models here.
admin.site.register(Book)
admin.site.register(BookApplication)
admin.site.register(Genre)
