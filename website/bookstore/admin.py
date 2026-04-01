from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(StudentClass)
admin.site.register(Subject)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Brand)
admin.site.register(BookType)
admin.site.register(Publisher)

admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)