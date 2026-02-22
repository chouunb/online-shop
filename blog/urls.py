from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name='product_list'),
    path('products/category/<slug:category_slug>/', views.CategoryPostsView.as_view(), name="category_products"),
    path('products/tag/<slug:tag_slug>/', views.TagPostsView.as_view(), name="tag_products"),
    path('products/add/', views.create_product, name='new_product'),
    path('products/<slug:product_slug>/edit/', views.update_product, name="edit_product"),
    path('products/<slug:product_slug>/delete/', views.delete_product, name="remove_product"),
    path("products/<slug:product_slug>/", views.get_product_detail, name='product_detail'),
    path('', views.main_page_view, name='main_page'),
]