from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name='product_list'),
    path('products/category/<slug:category_slug>/', views.CategoryProductsView.as_view(), name="category_products"),
    path('products/tag/<slug:tag_slug>/', views.TagProductsView.as_view(), name="tag_products"),
    path('products/add/', views.CreateProductView.as_view(), name='new_product'),
    path('products/<slug:product_slug>/edit/', views.ProductUpdateView.as_view(), name="edit_product"),
    path('products/<slug:product_slug>/delete/', views.ProductDeleteView.as_view(), name="remove_product"),
    path("products/<slug:product_slug>/", views.ProductDetailView.as_view(), name='product_detail'),
    path('', views.MainPageView.as_view(), name='main_page'),
]