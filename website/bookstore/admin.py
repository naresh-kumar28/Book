from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(StudentClass)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Brand)
admin.site.register(BookType)
admin.site.register(Publisher)
admin.site.register(Product)