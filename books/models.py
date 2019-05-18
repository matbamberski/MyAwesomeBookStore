from django.db import models
from django.urls import reverse

DEFAULT_DESCRIPTION = 'This book has no description!'

class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return self.name + " " + self.surname

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author, related_name='books')
    categories = models.ManyToManyField(Category, related_name='books')
    description = models.TextField(default=DEFAULT_DESCRIPTION)

    def get_absolute_url(self):
        return reverse('book:home')

