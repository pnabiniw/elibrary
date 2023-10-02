from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.contrib import messages
from apps.core.pagination import CustomPagination
from apps.commons.utils import get_base_url
from .models import Book, Genre, BookApplication


class HomeView(ListView):
    template_name = 'main/home.html'
    pagination_class = CustomPagination

    def get_pagination(self):
        return self.pagination_class()

    def get_queryset(self):
        genre = self.request.GET.get('genre')
        search = self.request.GET.get('search')
        book_filter = {"count__gt": 0}
        exclude = dict()
        if self.request.user.is_authenticated:
            exclude = {"book_applications__user": self.request.user,
                       "book_applications__returned_date__isnull": True}
        if genre:
            book_filter.update(genre__uuid=genre)
        if search:
            book_filter.update(name__icontains=search)
        return Book.objects.filter(**book_filter).exclude(**exclude).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        pagination = self.get_pagination()
        qs = pagination.get_paginated_qs(view=self)
        paginated_qs = pagination.get_nested_pagination(qs, nested_size=2)
        context['book_lists'] = paginated_qs
        context['genre'] = Genre.objects.all()
        page_number, page_str = pagination.get_current_page(view=self)
        context[page_str] = 'active'
        context["next_page"] = page_number + 1
        context["prev_page"] = page_number - 1
        context['base_url'] = get_base_url(request=self.request)
        if page_number >= pagination.get_last_page(view=self):
            context["next"] = "disabled"
        if page_number <= 1:
            context["prev"] = "disabled"
        context['home_active'] = 'active'
        return context


class BookDetailView(DetailView):
    template_name = 'main/book_detail.html'
    queryset = Book.objects.all()
    slug_field = 'uuid'  # This must be a unique field from the table
    slug_url_kwarg = 'uuid'  # This must be exactly from the url
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Book Detail"
        return context


def book_request(request, uuid):
    try:
        book = Book.objects.get(uuid=uuid)
    except Book.DoesNotExist:
        messages.error(request, "Something Went Wrong!!")
        return redirect('books_home')
    if BookApplication.objects.filter(user=request.user, book=book, returned_date__isnull=True):
        messages.error(request, "You have not returned this book !!")
        return redirect('books_home')
    BookApplication.objects.get_or_create(user=request.user, book=book)
    messages.success(request, f"You Have Requested The Book {book.name.title()}")
    return redirect('books_home')


@method_decorator(login_required, name='dispatch')
class MyBooksView(ListView):
    template_name = 'main/my_books.html'
    context_object_name = 'book_requests'

    def get_queryset(self):
        filter_dict = dict(user=self.request.user)
        return BookApplication.objects.filter(**filter_dict)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_books_active"] = 'active'
        return context
