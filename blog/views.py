from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Product
from blog.forms import ProductForm


def get_product_list(request):
    products = Product.objects.all()

    return render(request, template_name='shop/product_list.html', context={'products': products})


def get_product_detail(request, product_id):
    return render(request, 'shop/product_detail.html', {"product": get_object_or_404(Product, id=product_id)})


def create_product(request):
    name = "Создать объявление"
    submit_button_text = 'Создать'

    form = ProductForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            product = form.save()

            return redirect('product_detail', product_id=product.id)
    
    return render(request, 'shop/product_form.html', {"form": form, 'name': name, 'submit_button_text': submit_button_text})



def update_product(request, product_id):
    name = "Редактировать объявление"
    submit_button_text = 'Сохранить'

    product = get_object_or_404(Product, id=product_id)   

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()

            return redirect("product_detail", product_id=product.id)
        else:
            return render(request, 'shop/product_form.html', context={"form": form, 'name': name, 'submit_button_text': submit_button_text})

    form = ProductForm(instance=product)

    return render(request, 'shop/product_form.html', context={"form": form, 'name': name, 'submit_button_text': submit_button_text})


def delete_product(request, product_id):
    get_object_or_404(Product, id=product_id).delete()

    return redirect("product_list")