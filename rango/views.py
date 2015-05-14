from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page

def about(request):
    return render(request, 'rango/about.html')

def category(request, category_name_slug):
    context_dict = { }

    try:
        cat = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = cat.name

        pages = Page.objects.filter(category=cat)

        context_dict['pages'] = pages
        context_dict['category'] = cat
    except Category.DoesNotExist:
        context_dict['category_name'] = category_name_slug

    return render(request, 'rango/category.html', context_dict)

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict  = { 'categories': category_list }

    return render(request, 'rango/index.html', context_dict)