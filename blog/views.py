from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Product


def get_product_list(request):
    products = Product.objects.all()

    return render(request, template_name='shop/product_list.html', context={'products': products})


def get_product_detail(request, product_id):
    return render(request, 'shop/product_detail.html', {"product": get_object_or_404(Product, id=product_id)})


def create_product(request):
    if request.method == "POST":
        name = request.POST.get('name').strip()
        description=request.POST.get('description').strip()
        price=request.POST.get('price')

        errors = {}

        if not name:
            errors['name'] = 'Название товара обязательно!'
        if not description:
            errors['description'] = 'Описание товара обязательно!'
        if not price:
            errors['price'] = 'Цена обязательна!'

        if not errors:
            product = Product.objects.create(name=name, description=description, price=price)

            return redirect('product_detail', product_id=product.id)
        else:
            context = {
            'errors': errors,
            'name': name,
            'description': description,
            'price': price
            }

            return render(request, 'shop/product_add.html', context)
        
    return render(request, 'shop/product_add.html')