from django import forms
from .models import Author, Category
import requests
from urllib.parse import urlencode, quote
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

fields = ['intitle', 'inauthor', 'publisher', 'subject', 'isbn', 'lccn', 'oclc']

def prepare_keywords(keywords):
    query_params = [':'.join((k,quote(v))) for (k,v) in keywords.items() if k in fields and v]
    return '+'.join(query_params)

class ImportBookForm(forms.Form):
    intitle = forms.CharField(max_length=40, required=False)
    inauthor = forms.CharField(max_length=40, required=False)
    publisher = forms.CharField(max_length=40, required=False)
    subject = forms.CharField(max_length=40, required=False)
    isbn = forms.CharField(max_length=13, required=False)
    lccn = forms.CharField(max_length=20, required=False)
    oclc = forms.CharField(max_length=20, required=False)

    def search(self):
        result = {}
        keywords = prepare_keywords(self.cleaned_data)
        endpoint = 'https://www.googleapis.com/books/v1/volumes?q={terms}&fields=items(volumeInfo(title,authors,categories,description))'
        url = endpoint.format(terms=keywords)
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            if result:
                result['success'] = True
            else:
                result['success'] = False
                result['code'] = 404
        else:
            result['success'] = False
            if response.status_code == 404:
                result['code'] = 404
        return result     

    def clean(self):
        cleaned_data = super(ImportBookForm, self).clean()
        if not self.has_changed():
            raise forms.ValidationError("Please fill al least one field!")
        return cleaned_data

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'surname']

    def clean(self):
        cleaned_data = super(AuthorForm, self).clean()
        author = Author.objects.filter(name=cleaned_data['name'], surname=cleaned_data['surname']).first()
        if author:
            raise forms.ValidationError("This author already exists!")
        return cleaned_data

class CreateAuthorForm(PopRequestMixin, CreateUpdateAjaxMixin, AuthorForm):
    class Meta:
        model = Author
        fields = ['name', 'surname']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        category = Category.objects.filter(category_name=cleaned_data['category_name']).first()
        if category:
            raise forms.ValidationError("This category already exists!")
        return cleaned_data

class CreateCategoryForm(PopRequestMixin, CreateUpdateAjaxMixin, CategoryForm):
    class Meta:
        model = Category
        fields = ['category_name']