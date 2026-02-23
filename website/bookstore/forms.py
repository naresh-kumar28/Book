from django.forms import ModelForm, DateInput

from .models import *

class CategoryInsertForm(ModelForm):
    class Meta:
        model = Category
        fields = ['cat_name', 'cat_slug']


class AuthorInsertForm(ModelForm):
    class Meta:
        model = Author
        fields = ['author_name', 'author_slug', 'author_image']


class BrandInsertForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name', 'brand_slug']


class BooktypeInsertForm(ModelForm):
    class Meta:
        model = BookType
        fields = ['name', 'slug']


class PublisherInsertForm(ModelForm):
    class Meta:
        model = Publisher
        fields = ['publisher_name', 'publisher_slug', 'publisher_image']


class ProductInsertForm(ModelForm):
    class Meta:
        model = Product
        fields = [
                'category', 'author', 
                'brand', 'book_type', 
                'publisher', 'student_class', 'title', 
                'slug', 'description', 
                'image', 'cover_image', 
                'price', 'discount_price', 
                'language', 'pages', 'isbn', 
                'binding_type', 'width', 
                'height', 'weight', 
                'publish_date', 
                'quality_check', 'status'
        ]
        widgets = {
            'publish_date': DateInput(attrs={'type': 'date'}),
        }


class ClassInsertForm(ModelForm):
    class Meta:
        model = StudentClass
        fields = ['name', 'slug']