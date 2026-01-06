from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Product
from blog.forms import ProductForm


def get_product_list(request):
    products = Product.objects.all()

    return render(request, template_name='shop/product_list.html', context={'products': products})


def get_product_detail(request, product_id):
    return render(request, 'shop/product_detail.html', {"product": get_object_or_404(Product, id=product_id)})


def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            product = Product.objects.create(
                name=form.cleaned_data['name'], 
                description=form.cleaned_data['description'], 
                price=form.cleaned_data['price']
                )
                
            return redirect('product_detail', product_id=product.id)
        else:
            return render(request, 'shop/product_add.html', {"form": form})
        

    form = ProductForm()

    return render(request, 'shop/product_add.html', {"form": form})
