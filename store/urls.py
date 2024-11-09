from django.urls import path, include

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('get-subcategories/<int:category_id>/', views.get_subcategories, name='get_subcategories'),

]
