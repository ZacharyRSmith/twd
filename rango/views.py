from django.http import HttpResponse
from django.shortcuts import render
from rango.forms import CategoryForm
from rango.models import Category, Page

def about(request):
    return render(request, 'rango/about.html')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', { 'form': form })

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
    most_visited_pages = Page.objects.order_by('-views')[:5]
    context_dict  = { 'categories': category_list,
                      'most_visited_pages': most_visited_pages }

    return render(request, 'rango/index.html', context_dict)
