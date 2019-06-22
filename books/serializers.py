from rest_framework import serializers
from .models import Book, Author, Category, DEFAULT_DESCRIPTION


def json2obj(result):
    if result['success'] and 'items' in result:
        json = result['items']
        for volumen in json:
            authors = []
            if 'authors' in volumen['volumeInfo']:
                for author in volumen['volumeInfo']['authors']:
                    author_name = author.split()
                    data_author = {
                        'name': " ".join(author_name[:-1]),
                        'surname': author_name[-1]
                    }
                    author_obj = Author.objects.filter(
                        name=data_author['name'],
                        surname=data_author['surname']
                        ).first()
                    if not author_obj:
                        author_obj = Author.objects.create(**data_author)
                    author_obj.save()
                    authors.append(author_obj)

            categories = []
            if 'categories' in volumen['volumeInfo']:
                for category in volumen['volumeInfo']['categories']:
                    data_category = {
                        'category_name': category
                    }
                    category_obj = Category.objects.filter(
                        category_name=data_category['category_name']
                        ).first()
                    if not category_obj:
                        category_obj = Category.objects.create(**data_category)
                    category_obj.save()
                    categories.append(category_obj)

            description = DEFAULT_DESCRIPTION
            if 'description' in volumen['volumeInfo']:
                description = volumen['volumeInfo']['description']

            new_book = Book.objects.filter(
                title=volumen['volumeInfo']['title'],
                description=description
                ).first()
            if not new_book:
                new_book = Book.objects.create(
                    title=volumen['volumeInfo']['title'],
                    description=description
                    )
                new_book.save()
                new_book.authors.add(*authors)
                new_book.categories.add(*categories)


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'surname')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name')


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'authors', 'categories', 'description')
        