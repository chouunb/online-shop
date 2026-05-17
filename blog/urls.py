from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name='product_list'),
    path("products/load-more/", views.load_more_products_view, name="load_more_products"),
    path("products/search/", views.ProductSearchView.as_view(), name="product_search"),
    path('products/category/<slug:category_slug>/', views.CategoryProductsView.as_view(), name="category_products"),
    path('products/tag/<slug:tag_slug>/', views.TagProductsView.as_view(), name="tag_products"),
    path('products/add/<int:product_id>/', views.add_to_cart_view, name="add_to_cart"),
    path('products/remove/<int:product_id>/', views.remove_from_cart_view, name="remove_from_cart"),
    path('products/delete/<int:product_id>/',views.delete_cart_item_view, name='delete_cart_item'),
    path("products/<int:product_id>/review/add/", views.add_review_view, name="add_review"),
    path("products/<int:product_id>/reviews/load-more/", views.load_more_reviews_view, name="load_more_reviews"),
    path('products/add/', views.CreateProductView.as_view(), name='new_product'),
    path('products/<slug:product_slug>/edit/', views.ProductUpdateView.as_view(), name="edit_product"),
    path('products/<slug:product_slug>/delete/', views.ProductDeleteView.as_view(), name="remove_product"),
    path("products/<slug:product_slug>/", views.ProductDetailView.as_view(), name='product_detail'),
    path('', views.MainPageView.as_view(), name='main_page'),
]
