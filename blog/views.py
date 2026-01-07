from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from blog.models import Product
from blog.forms import ProductForm


def get_product_list(request):
    products = Product.objects.all()

    return render(request, template_name='shop/product_list.html', context={'products': products})


def get_product_detail(request, product_id):
    return render(request, 'shop/product_detail.html', {"product": get_object_or_404(Product, id=product_id)})

@login_required
def create_product(request):
    name = "Создать объявление"
    submit_button_text = 'Создать'

    form = ProductForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            product = form.save()

            return redirect('blog:product_detail', product_id=product.id)
    
    return render(request, 'shop/product_form.html', {"form": form, 'name': name, 'submit_button_text': submit_button_text})



def update_product(request, product_id):
    name = "Редактировать объявление"
    submit_button_text = 'Сохранить'

    product = get_object_or_404(Product, id=product_id)   

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()

            return redirect("blog:product_detail", product_id=product.id)
        else:
            return render(request, 'shop/product_form.html', context={"form": form, 'name': name, 'submit_button_text': submit_button_text})

    form = ProductForm(instance=product)

    return render(request, 'shop/product_form.html', context={"form": form, 'name': name, 'submit_button_text': submit_button_text})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.delete()
        return redirect("blog:product_list")

    return render(request, 'shop/confirm_product_delete.html', {'product': product})