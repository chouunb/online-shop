from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from unidecode import unidecode
from django.views.generic import ListView

from blog.models import Product, Category, Tag
from blog.forms import ProductForm


class ProductListView(ListView):
    template_name = 'shop/pages/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(status="published")


def get_category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, status='published')
    
    context = {
    'category': category,
    'products': products
    }
    return render(request, 'shop/pages/category_products.html', context)



def get_tag_products(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    products = Product.objects.filter(tags=tag, status='published')

    return render(request, 'shop/pages/tag_products.html', {
        'tag': tag,
        'products': products
    })


def get_product_detail(request, product_slug):
    return render(request, 'shop/pages/product_detail.html', {"product": get_object_or_404(Product, slug=product_slug)})

@login_required
def create_product(request):
    name = "Создать объявление"
    submit_button_text = 'Создать'

    form = ProductForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.slug = slugify(unidecode(product.name))
            product.save()

            tags = form.cleaned_data.get('tags_input')

            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                product.tags.add(tag)

            return redirect('blog:product_detail', product_slug=product.slug)
    
    return render(request, 'shop/pages/product_form.html', {"form": form, 'name': name, 'submit_button_text': submit_button_text})



def update_product(request, product_slug):
    name = "Редактировать объявление"
    submit_button_text = 'Сохранить'

    product = get_object_or_404(Product, slug=product_slug)   

    if (request.user != product.seller):
        return render(request, 'shop/pages/not_allowed.html')

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            tags = form.cleaned_data.get('tags_input')
            product.tags.clear()
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                product.tags.add(tag)

            return redirect("blog:product_detail", product_slug=product.slug)
        else:
            return render(request, 'shop/pages/product_form.html', context={"form": form, 'name': name, 'submit_button_text': submit_button_text})

    existing_tags = ", ".join(tag.name for tag in product.tags.all())
    form = ProductForm(instance=product, initial={'tags_input': existing_tags})

    return render(request, 'shop/pages/product_form.html', context={"form": form, 'name': name, 'submit_button_text': submit_button_text})


def delete_product(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)

    if (request.user != product.seller):
        return render(request, 'shop/pages/not_allowed.html')

    if request.method == "POST":
        product.delete()
        return redirect("blog:product_list")

    return render(request, 'shop/pages/confirm_product_delete.html', {'product': product})

def main_page_view(request):
    return render(request, template_name='shop/pages/main_page.html')