from django.urls import path
from .views import HomeView, BookDetailView, book_request, MyBooksView

urlpatterns = [
    path('book-detail/<str:uuid>/', BookDetailView.as_view(), name='book_detail'),
    path('book-request/<str:uuid>/', book_request, name='book_request'),
    path('my-books/', MyBooksView.as_view(), name='my_books'),
    path('', HomeView.as_view(), name='books_home')
]
