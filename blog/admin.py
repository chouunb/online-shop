from django.contrib import admin

from blog.models import Product, Category, Tag

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
