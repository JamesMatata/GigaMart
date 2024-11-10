from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('get-subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),
    path('category/<str:category_slug>/', views.category_list, name='category_list'),
    path('category/<str:category_slug>/<str:subcategory_slug>/', views.subcategory_list, name='subcategory_list'),
]
