from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode

User = get_user_model()


class Product(models.Model):
    STATUS_CHOICES = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )
    
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, editable=False, verbose_name="Слаг")
    category = models.ForeignKey(
        'Category',
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )
    tags = models.ManyToManyField("Tag", related_name='products', blank=True, verbose_name='Теги')
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена")
    image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    status = models.CharField(choices=STATUS_CHOICES, default='draft', verbose_name="Статус")

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        db_table = "shop_products"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, editable=False, verbose_name="Слаг")

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_products', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"
        db_table = "shop_categories"


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, editable=False, verbose_name='Слаг')

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))

        super().save(*args, **kwargs)

    def __str__(self):
        return f'#{self.name}'
    
    def get_absolute_url(self):
        return reverse('blog:tag_products', args=[self.slug])

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = "Теги"
        db_table = "shop_tags"
