from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    STATUS_CHOICES = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )
    
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, editable=False, verbose_name="Слаг")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена")
    image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    status = models.CharField(choices=STATUS_CHOICES, default='draft', verbose_name="Статус")

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        db_table = "shop_products"

    def __str__(self):
        return self.name
