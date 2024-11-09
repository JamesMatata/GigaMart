from django.http import JsonResponse
from django.shortcuts import render

from store.models import Category, Subcategory


def index(request):
    return render(request, 'store/index.html', {})


def get_subcategories(request, category_id):
    category = Category.objects.get(pk=category_id)
    subcategories = Subcategory.objects.filter(category=category).values('id', "name")
    return JsonResponse(list(subcategories), safe=False)
