from django.shortcuts import render, get_object_or_404

from blog.models import Product


def get_product_list(request):
    products = Product.objects.all()

    return render(request, template_name='blog/product_list.html', context={'products': products})


def get_post_detail(request, product_id):
    return render(request, 'blog/product_detail.html', {"product": get_object_or_404(Product, id=product_id)})