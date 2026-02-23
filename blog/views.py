from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from unidecode import unidecode
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Product, Category, Tag
from blog.forms import ProductForm


class ProductListView(ListView):
    template_name = 'shop/pages/product_list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(status="published")


class CategoryProductsView(ListView):
    template_name = 'shop/pages/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Product.objects.filter(category=self.category, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = self.category
        
        return context


class TagProductsView(ListView):
    template_name = 'shop/pages/tag_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Product.objects.filter(tags=self.tag, status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tag'] = self.tag

        return context


class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = 'product_slug'
    template_name = 'shop/pages/product_detail.html'


class CreateProductView(LoginRequiredMixin, CreateView):
    form_class = ProductForm
    template_name = 'shop/pages/product_form.html'
    extra_context = {
        'title': "Создать объявление",
        'submit_button_text': "Создать"
    }

    def form_valid(self, form):
        product = form.save(commit=False)
        product.seller = self.request.user
        product.save()


        tags = form.cleaned_data.get('tags_input')
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            product.tags.add(tag)

        return redirect('blog:product_detail', product_slug=product.slug)


class ProductUpdateView(UpdateView):
    model = Product
    slug_url_kwarg = 'product_slug'
    form_class = ProductForm
    template_name = 'shop/pages/product_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Редактировать объявление"
        context['submit_button_text'] = "Сохранить"
        context['form'].fields['tags_input'].initial = ", ".join(tag.name for tag in self.object.tags.all())
        
        return context

    def form_valid(self, form):
        if (self.request.user != self.object.seller):
            return render(self.request, 'shop/pages/not_allowed.html')

        form.save()

        tags = form.cleaned_data.get('tags_input', [])
        self.object.tags.clear()
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            self.object.tags.add(tag)

        return redirect('blog:product_detail', product_slug = self.object.slug)


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