import os
import secrets
import string
import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.text import slugify

from GigaMart import settings

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
    short_description = models.TextField(null=True)
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
    image = models.ImageField(upload_to='products', default='products/default.jpg')

    class Meta:
        verbose_name_plural = 'ProductImages'

    def __str__(self):
        return f"Additional image for {self.product.name}"


def generate_unique_id():
    # Generate a random 12-character alphanumeric string
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(12))


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Completed', 'Completed'),
    ]

    unique_id = models.CharField(max_length=12, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    inquiry = models.ForeignKey('Inquiry', on_delete=models.SET_NULL, null=True, blank=True, to_field='unique_id')
    order_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Orders'

    def save(self, *args, **kwargs):
        if not self.unique_id:  # Generate unique_id only if it isn't set
            self.unique_id = generate_unique_id()
        super().save(*args, **kwargs)

        # Check if the order status is being changed to 'Completed'
        original = Order.objects.filter(pk=self.pk).first()
        if original and original.order_status != 'Completed' and self.order_status == 'Completed':
            self.update_product_inventory()

    def update_product_inventory(self):
        if not self.inquiry:
            return
        for item in self.inquiry.items:
            product_id = item.get('product_id')
            qty = item.get('qty', 0)
            try:
                product = Product.objects.get(id=product_id)
                if product.items_remaining >= qty:
                    product.items_remaining -= qty
                    product.traded_count += qty
                    product.save()
                else:
                    raise ValueError(
                        f"Insufficient stock for product {product.name}. Available: {product.items_remaining}, Requested: {qty}"
                    )
            except Product.DoesNotExist:
                raise ValueError(f"Product with ID {product_id} not found.")
            except Exception as e:
                raise RuntimeError(f"Error updating product inventory: {str(e)}")

    def __str__(self):
        user_display = self.user.username if self.user else 'Guest'
        return f"Order {self.unique_id} by {user_display}"

    def order_confirmation_email(self):
        """Send confirmation email to the user."""
        context = {
            'user': {'first_name': self.inquiry.name if self.inquiry else 'Guest'},
            'domain': '127.0.0.1:8000/',  # Replace with your domain
            'unique_id': self.unique_id,
            'items': self.inquiry.items if self.inquiry else [],
        }
        subject = f"Order {self.unique_id} Creation"
        message = render_to_string('emails/order_creation.html', context)

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.inquiry.email] if self.inquiry else [],
        )
        email.content_subtype = 'html'
        email.send()


@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    """Send confirmation email after the order is created."""
    if created:  # Only send email for new orders
        instance.order_confirmation_email()


class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Canceled', 'Canceled'),
    ]

    unique_id = models.CharField(max_length=12, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inquiries", null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    items = models.JSONField()
    inquiry_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    inquiry_whatsapp_link = models.URLField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        user_display = self.user.username if self.user else 'Guest'
        return f"Inquiry {self.unique_id} by {user_display}"

    def save(self, *args, **kwargs):
        if not self.unique_id:  # Ensure unique_id is only generated if not already set
            self.unique_id = generate_unique_id()

        if self.pk and Inquiry.objects.filter(pk=self.pk).exists():
            original = Inquiry.objects.get(pk=self.pk)
            if original.inquiry_status != 'Approved' and self.inquiry_status == 'Approved':
                Order.objects.create(
                    inquiry=self,
                    user=self.user,
                    order_status='Pending'
                )

        super().save(*args, **kwargs)

    def send_confirmation_email(self):
        """Send confirmation email to the user."""
        context = {
            'user': {'first_name': self.name},
            'domain': '127.0.0.1:8000/',  # Replace with your domain
            'unique_id': self.unique_id,
            'items': self.items,
        }
        subject = f"Inquiry {self.unique_id} Creation"
        message = render_to_string('emails/inquiry_creation.html', context)

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.email],
        )
        email.content_subtype = 'html'  # Specify the email content as HTML
        email.send()


@receiver(post_save, sender=Inquiry)
def handle_inquiry_post_save(sender, instance, created, **kwargs):
    """Handle actions after an Inquiry is saved."""
    if created:
        # Send a confirmation email for newly created inquiries
        instance.send_confirmation_email()


class CheckoutSession(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    county = models.CharField(max_length=100)
    step = models.CharField(max_length=50, default='summary')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Checkout session for {self.first_name} {self.last_name}"
