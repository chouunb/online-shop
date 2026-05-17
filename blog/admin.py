from django.contrib import admin

from blog.models import Product, Category, Tag, CartItem, Review

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(CartItem)
admin.site.register(Review)
