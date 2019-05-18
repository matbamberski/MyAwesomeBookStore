from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_filter_list, name='home'),
    path('new/', views.BookCreateView.as_view(), name='book-create'),
    path('import/', views.google_api, name='book-import'),
    path('filter/', views.BookListing.as_view(), name='listing'),
    path('newauthor/', views.AddAuthor.as_view(), name='add-author'),
    path('newcategory/', views.AddCategory.as_view(), name='add-category'),
]