from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Category Name')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='Category Slug')

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Product Name')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='Product Slug')
    description = models.TextField(blank=True, null=True, verbose_name='Product Description')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Product Image')
    price = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name='Product Price')
    discount = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name='Product Discount in %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Product Quantity')
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT, verbose_name='Product Category')

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.name}, {self.category.name}, Quantity: {self.quantity}'