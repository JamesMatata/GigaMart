from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('get-subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
    path('category/<str:category_slug>/', views.category_list, name='category_list'),
    path('category/<str:category_slug>/<str:subcategory_slug>/', views.subcategory_list, name='subcategory_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('search/', views.search_results, name='search_results'),
]
