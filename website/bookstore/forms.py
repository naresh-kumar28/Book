from django.forms import ModelForm

from .models import *

class CategoryInsertForm(ModelForm):
    class Meta:
        model = Category
        fields = ['cat_name', 'cat_slug']


class AuthorInsertForm(ModelForm):
    class Meta:
        model = Author
        fields = ['author_name', 'author_slug', 'author_image']
