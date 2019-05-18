from django.views.generic import ListView, CreateView, DeleteView
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from django.urls import reverse_lazy
from .models import Book, Category, Author
from .forms import ImportBookForm, CreateAuthorForm, CreateCategoryForm
from .serializers import json2obj, AuthorSerializer, CategorySerializer, BookSerializer
from .pagination import StandartResutlsSetPagination
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from bootstrap_modal_forms.mixins import PassRequestMixin
# from bootstrap_modal_forms.generic import BSModalDeleteView
import json


class BookListView(ListView):
    model = Book
    context_object_name = 'books'

class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'authors', 'categories', 'description']

class AddAuthor(PassRequestMixin, SuccessMessageMixin, CreateView):
    form_class = CreateAuthorForm
    template_name = 'books/add_author.html'
    success_url = reverse_lazy('book:book-create')

class AddCategory(PassRequestMixin, SuccessMessageMixin, CreateView):
    form_class = CreateCategoryForm
    template_name = 'books/add_category.html'
    success_url = reverse_lazy('book:book-create')

# class BookDeleteView(BSModalDeleteView, DeleteView):
#     model = Book
#     template_name = 'books/delete_book.html'
#     success_url = reverse_lazy('book')

def google_api(request):
    result = {}
    if 'intitle' in request.GET:
        form = ImportBookForm(request.GET)
        if form.is_valid():
            result = form.search()
            json2obj(result)
            if result['success']:
                messages.success(request, f"{len(result['items'])} books added BookStore!")
            elif result['code'] and result['code'] == 404:
                messages.warning(request, f"Books not found!")
            else:
                messages.warning(request, f'API is not available')
    else:
        form = ImportBookForm()
    return render(request, 'books/book_import.html', {'form' : form, 'result' : result})

def book_filter_list(request):
    return render(request, 'books/home.html', {})

class BookListing(ListAPIView):
    pagination_class = StandartResutlsSetPagination
    serializer_class = BookSerializer

    def get_queryset(self):
        query_list = Book.objects.all()
        category = self.request.query_params.get('category', None)
        author = self.request.query_params.get('author', None)
        # print(author, category)
        try:
            authors = Author.objects.filter(
                Q(surname__icontains=author) | Q(name__icontains=author)
            )
            categories = Category.objects.filter(category_name__icontains=category)
        except:
            return query_list
        
        query_list = query_list.filter(
            authors__in=authors
            )
        if category:
            query_list = query_list.filter(
            categories__in=categories
            )
        # print(query_list)
        return query_list.distinct()
