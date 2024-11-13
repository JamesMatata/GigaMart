import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='categories/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    image = models.ImageField(upload_to='subcategories/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:subcategory_list', args=[self.category.slug, self.slug])

    class Meta:
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return self.name


@receiver(pre_delete, sender=Category)
def delete_category_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(pre_delete, sender=Subcategory)
def delete_subcategory_image(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Product(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=255)
    description = models.TextField(null=True)
    key_features = models.JSONField(null=True)
    specifications = models.JSONField(null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey('Subcategory', on_delete=models.SET_NULL, null=True, blank=True)
    traded_count = models.IntegerField(default=0)
    items_remaining = models.IntegerField(default=0)
    warrant_months = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)])
    main_image = models.ImageField(upload_to='products')

    users_wishlist = models.ManyToManyField(User, related_name="user_wishlist", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        # Ensure there are exactly 4 additional images
        if self.pk and self.additional_images.count() != 4:
            raise ValidationError("Exactly 4 additional images are required for each product.")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Products'

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    def __str__(self):
        return self.name


# Signal receiver to delete product images when a Product is deleted
@receiver(pre_delete, sender=Product)
def remove_product_images(sender, instance, **kwargs):
    if instance.main_image:
        if os.path.isfile(instance.main_image.path):
            os.remove(instance.main_image.path)

    for image in instance.additional_images.all():
        if image.image:
            if os.path.isfile(image.image.path):
                os.remove(image.image.path)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="additional_images")
    image = models.ImageField(upload_to='products')

    class Meta:
        verbose_name_plural = 'ProductImages'

    def __str__(self):
        return f"Additional image for {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    inquiry = models.ForeignKey('Inquiry', on_delete=models.SET_NULL, null=True, blank=True)
    order_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = 'OrderItems'

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inquiries")
    items = models.JSONField()
    inquiry_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"Inquiry {self.id} by {self.user.username}"