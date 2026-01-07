from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path("products/", views.get_product_list, name='product_list'),
    path("products/<int:product_id>/", views.get_product_detail, name='product_detail'),
    path('products/add/', views.create_product, name='new_product'),
    path('products/<int:product_id>/edit/', views.update_product, name="edit_product"),
    path('products/<int:product_id>/delete/', views.delete_product, name="remove_product"),
]