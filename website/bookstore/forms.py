from django.forms import ModelForm, DateInput
from django import forms

from .models import *

class CategoryInsertForm(ModelForm):
    class Meta:
        model = Category
        exclude = ['cat_slug']


class AuthorInsertForm(ModelForm):
    class Meta:
        model = Author
        exclude = ['author_slug']


class BrandInsertForm(ModelForm):
    class Meta:
        model = Brand
        exclude = ['brand_slug']


class BooktypeInsertForm(ModelForm):
    class Meta:
        model = BookType
        exclude = ['slug']


class PublisherInsertForm(ModelForm):
    class Meta:
        model = Publisher
        exclude = ['publisher_slug']


class ProductInsertForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductInsertForm, self).__init__(*args, **kwargs)
        
        # In sabhi dropdowns ka default "hyphen" hatakar mast label laga diya hai
        self.fields['category'].empty_label = "Select Category"
        self.fields['author'].empty_label = "Select Author"
        self.fields['brand'].empty_label = "Select Brand"
        self.fields['book_type'].empty_label = "Select Book Type"
        self.fields['publisher'].empty_label = "Select Publisher"
        self.fields['student_class'].empty_label = "Select Class/Grade"
        self.fields['subject'].empty_label = "Select Subject"
    class Meta:
        model = Product
        exclude = ['slug']
        widgets = {
            'publish_date': DateInput(attrs={'type': 'date'}),
        }
        

class ClassInsertForm(ModelForm):
    class Meta:
        model = StudentClass
        exclude = ['slug']


class SubjectInsertForm(ModelForm):
    class Meta:
        model = Subject
        exclude = ['subject_slug']


class CouponInsertForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ["code", "discount_amount", "valid_from", "valid_to"]
        widgets = {
            "code": forms.TextInput(attrs={"placeholder": "Enter Coupon Code"}),
            "valid_from": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "valid_to": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }