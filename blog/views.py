from django.shortcuts import render

from blog.models import Product


def get_products_list(request):
    products = Product.objects.all()

    return render(request, template_name='blog/product_list.html', context={'products': products})

