from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from unidecode import unidecode
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from blog.models import Product, Category, Tag, CartItem, Review
from blog.forms import ProductForm


class ProductListView(ListView):
    template_name = 'shop/pages/product_list.html'
    context_object_name = 'products'
    products_per_batch = 6

    def get_queryset(self):

        queryset = Product.objects.filter(
            status="published"
        )

        if self.request.user.is_authenticated:

            queryset = queryset.prefetch_related(
                Prefetch(
                    'cart_items',
                    queryset=CartItem.objects.filter(
                        user=self.request.user
                    ),
                    to_attr='user_cart_items'
                )
            )

        self.products_query = queryset.order_by('-created_at')

        return self.products_query[:self.products_per_batch]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["has_more_products"] = (
            self.products_query.count() > self.products_per_batch
        )

        context["products_per_batch"] = self.products_per_batch

        return context



def load_more_products_view(request):
    offset = int(request.GET.get("offset", 0))
    products_per_batch = ProductListView.products_per_batch

    products_query = Product.objects.filter(status="published").order_by('-created_at')
    products = products_query[offset:offset + products_per_batch]

    products_html_string = ''.join([
        render_to_string("shop/includes/product_container.html", {"product": product}, request)
        for product in products
    ])

    has_more_products = offset + products_per_batch < products_query.count()

    return JsonResponse({
        'html': products_html_string,
        'has_more': has_more_products
    })


class ProductSearchView(ListView):
    template_name = "shop/pages/product_search.html"
    context_object_name = 'products'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_performed'] = any(self.request.GET.keys())
        return context

    def get_queryset(self):
        search_query = self.request.GET.get("search")

        queryset = Product.objects.filter(
            status="published"
        )
        if self.request.user.is_authenticated:

            queryset = queryset.prefetch_related(
                Prefetch(
                    'cart_items',
                    queryset=CartItem.objects.filter(
                        user=self.request.user
                    ),
                    to_attr='user_cart_items'
                )
            )

        if search_query:
            query = (
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

            search_category = self.request.GET.get("search_category")
            search_tag = self.request.GET.get("search_tag")

            if search_category:
                query |= Q(category__name__icontains=search_query)

            if search_tag:
                query |= Q(tags__name__icontains=search_query)

            return queryset.filter(query)

        return queryset.none()


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
    reviews_per_batch = 3


    def get_object(self, queryset=None):
        product = super().get_object(queryset)

        user = self.request.user
        session_key = f'product_{product.id}_viewed'
        if not self.request.session.get(session_key, False) and product.seller != user:
            Product.objects.filter(id=product.id).update(views=F("views") + 1)
            product.views = product.views + 1
            self.request.session[session_key] = True

        if user.is_authenticated and user != product.seller and not product.viewed_users.filter(id=user.id).exists():
            product.viewed_users.add(user)

        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        product = self.object

        context['in_cart'] = False
        context['cart_quantity'] = 0

        if user.is_authenticated:

            cart_item = CartItem.objects.filter(
                user=user,
                product=product
            ).first()

            if cart_item:
                context['in_cart'] = True
                context['cart_quantity'] = cart_item.quantity

            reviews_query = product.reviews.all().order_by('-created_at')
            context["reviews"] = reviews_query[:self.reviews_per_batch]
            context["has_more_reviews"] = (
                reviews_query.count() > self.reviews_per_batch
            )
            context["reviews_per_batch"] = self.reviews_per_batch

        return context


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

        messages.success(self.request, 'Объявление успешно создано!')

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


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    slug_url_kwarg = 'product_slug'
    template_name = 'shop/pages/confirm_product_delete.html'
    success_url = reverse_lazy('blog:product_list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if request.user != self.object.seller:
            return render(request, 'shop/pages/not_allowed.html')
        
        return super().dispatch(request, *args, **kwargs)


class MainPageView(TemplateView):
    template_name = 'shop/pages/index.html'


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@login_required
def add_to_cart_view(request, product_id):

    if request.method != 'POST':
        return JsonResponse({
            'error': 'Только POST запрос'
        }, status=400)

    product = get_object_or_404(Product, id=product_id)

    # Нельзя добавлять свой товар
    if product.seller == request.user:
        return JsonResponse({
            'error': 'Нельзя добавить свой товар в корзину'
        }, status=403)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    # Если товар уже есть — увеличиваем количество
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({
        'success': True,
        'quantity': cart_item.quantity,
        'product_id': product.id
    })


@login_required
def remove_from_cart_view(request, product_id):

    if request.method != 'POST':
        return JsonResponse({
            'error': 'Только POST запрос'
        }, status=400)

    product = get_object_or_404(Product, id=product_id)

    cart_item = get_object_or_404(
        CartItem,
        user=request.user,
        product=product
    )

    # Уменьшаем количество
    if cart_item.quantity > 1:

        cart_item.quantity -= 1
        cart_item.save()

        quantity = cart_item.quantity

    else:
        cart_item.delete()

        quantity = 0

    return JsonResponse({
        'success': True,
        'quantity': quantity,
        'product_id': product.id
    })

@require_POST
@login_required
def delete_cart_item_view(request, product_id):

    cart_item = get_object_or_404(
        CartItem,
        user=request.user,
        product_id=product_id
    )

    cart_item.delete()

    return JsonResponse({
        'success': True
    })


@login_required
@require_POST
def add_review_view(request, product_id):

    text = request.POST.get('text', '').strip()
    rating = int(request.POST.get('rating', 5))

    if not text:
        return JsonResponse({
            'success': False,
            'error': 'Текст отзыва не может быть пустым'
        })

    product = get_object_or_404(Product, id=product_id)

    # Нельзя оставлять отзыв на свой товар
    if product.seller == request.user:
        return JsonResponse({
            'success': False,
            'error': 'Нельзя оставлять отзыв на свой товар'
        }, status=403)

    review = Review.objects.create(
        product=product,
        author=request.user,
        text=text,
        rating=rating
    )

    review_html = render_to_string(
        'shop/includes/review_container.html',
        {'review': review},
        request=request
    )

    return JsonResponse({
        'success': True,
        'review_html': review_html,
        'reviews_count': product.reviews.count()
    })


def load_more_reviews_view(request, product_id):

    from time import sleep
    sleep(0.5)

    offset = int(request.GET.get("offset"))

    reviews_per_batch = (
        ProductDetailView.reviews_per_batch
    )

    product = get_object_or_404(
        Product,
        id=product_id
    )

    reviews_query = (
        product.reviews.all()
        .order_by('-created_at')
    )

    reviews = reviews_query[
        offset:offset + reviews_per_batch
    ]

    reviews_html = ''.join([
        render_to_string(
            "shop/includes/review_container.html",
            {"review": review},
            request
        )
        for review in reviews
    ])

    has_more_reviews = (
        offset + reviews_per_batch
        < reviews_query.count()
    )

    return JsonResponse({
        'html': reviews_html,
        'has_more': has_more_reviews
    })