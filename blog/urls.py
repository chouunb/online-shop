from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.get_product_list, name='product_list'),
    path("products/<int:product_id>/", views.get_product_detail, name='product_detail'),
]