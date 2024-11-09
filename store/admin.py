from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Category, Subcategory, Product, OrderItem, Order, Inquiry, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    search_fields = ('name',)
    ordering = ('id',)


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'image')
    list_filter = ('category',)
    search_fields = ('name',)
    ordering = ('id',)


class ProductImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        images_count = sum(1 for form in self.forms if form.cleaned_data and not form.cleaned_data.get('DELETE', False))
        if images_count != 4:
            raise ValidationError("Please upload exactly 4 additional images for each product.")


class ProductAdminForm(forms.ModelForm):
    key_features = forms.JSONField(
        widget=forms.Textarea(attrs={
            'rows': 5, 'cols': 40,
            'placeholder': '[ "Key Feature 1: Description", "Key Feature 2: Description"]'
        }),
        help_text='Enter each key feature as a string in the format: ["Feature: Description"]'
    )

    specifications = forms.JSONField(
        widget=forms.Textarea(attrs={
            'rows': 10, 'cols': 40,
            'placeholder': '{"Category": {"Key": "Value"}}'
        }),
        help_text='Enter the specifications as a JSON object. Example: {"Display": {"Size": "5.8 inches", '
                  '"Type": "OLED"}}'
    )

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    formset = ProductImageInlineFormSet
    extra = 4
    max_num = 4
    fields = ('image',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm  # Use the custom form to handle fields

    # List display of all important fields
    list_display = (
        'id', 'name', 'price', 'brand', 'category', 'subcategory', 'traded_count', 'items_remaining', 'discount'
    )
    list_filter = ('brand', 'category', 'subcategory')
    search_fields = ('name', 'brand', 'category__name', 'subcategory__name')
    ordering = ('id',)
    readonly_fields = ('traded_count',)

    # Fieldsets to include all fields in the product admin form
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'brand', 'category', 'subcategory', 'main_image', 'description', 'key_features',
                       'specifications')
        }),
        ('Stock & Trade Info', {
            'fields': ('traded_count', 'items_remaining', 'discount')
        }),
    )

    # Add custom JavaScript to filter subcategories and validate fields
    class Media:
        js = ('js/category_subcategory_filter.js',)

    # Inline for additional product images
    inlines = [ProductImageInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0  # Disable extra empty fields
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_status', 'created_at')
    list_filter = ('order_status', 'created_at')
    search_fields = ('user__username', 'id')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'inquiry_status', 'created_at')
    list_filter = ('inquiry_status', 'created_at')
    search_fields = ('user__username', 'id')
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
    ordering = ('order',)
