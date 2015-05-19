from rango.bing_search import run_query
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page

def about(request):
    context_dict = { 'visits': request.session['visits'] }
    return render(request, 'rango/about.html', context_dict)

@login_required
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

@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        print "1!"
        form = PageForm(request.POST)

        if form.is_valid():
            print "2!"
            if cat:
                print "3!"
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # TODO Redirect
                return category(request, category_name_slug)
        else:
            print "4!"
            print form.errors
    else:
        print "5!"
        form = PageForm()

    print "6!"
    context_dict = { 'category': cat, 'category_name_slug': category_name_slug, 'form': form }
    return render(request, 'rango/add_page.html', context_dict )

def category(request, category_name_slug):
    context_dict = { 'query': None, 'result_list': None }

    if request.method == "POST":
        query = request.POST['query'].strip()
        if query:
            context_dict['query'] = query
            context_dict['result_list'] = run_query(query)

    try:
        cat = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = cat.name
        context_dict['category_name_slug'] = category_name_slug

        pages = Page.objects.filter(category=cat).order_by('-views')

        context_dict['pages'] = pages
        context_dict['category'] = cat
    except Category.DoesNotExist:
        context_dict['category_name'] = category_name_slug

    if not context_dict['query']:
        context_dict['query'] = cat.name

    return render(request, 'rango/category.html', context_dict)

def category_index(request):
    try:
        categories = Category.objects.all()
    except:
        Category.DoesNotExist
        categories = None

    context_dict = { 'categories': categories }
    return render(request, 'rango/category_index.html', context_dict)

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    most_visited_pages = Page.objects.order_by('-views')[:5]
    context_dict  = { 'categories': category_list,
                      'most_visited_pages': most_visited_pages }

    visits = request.session.get('visits')
    if not visits:
        visits = 1

    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 5:
            reset_last_visit_time = True
            visits += 1
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits']     = visits

    context_dict['visits'] = visits

    return render(request, 'rango/index.html', context_dict)

@login_required
def like_category(request):
#      context_dict = { 'query': None, 'result_list': None }

    if request.method != "GET" or 'category_id' not in request.GET:
        # FIXME Msg user
        return redirect('/rango/')

    try:
        cat = Category.objects.get(id=int(request.GET['category_id']))
        cat.likes += 1
        cat.save()

        return HttpResponse(cat.likes)
    except Category.DoesNotExist:
        # FIXME Msg user
        return redirect('/rango/')

    # FIXME Code should never reach this return
    return redirect('/rango/')

def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if not starts_with:
        return cat_list

    cat_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]

    return cat_list

# def register(request):
#     registered = False

#     if request.method == 'POST':
#         user_form    = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)

#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()

#             user.set_password(user.password)
#             user.save()

#             profile = profile_form.save(commit=False)
#             profile.user = user

#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']

#             profile.save()

#             registered = True
#         else:
#             print user_form.errors, profile_form.errors

#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()

#     return render(request,
#                  'rango/register.html',
#                  { 'user_form': user_form, 'profile_form': profile_form,
#                    'registered': registered })

def register_profile():
    pass

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', { })

# def search(request):
#     context_dict = { }

#     if request.method == "POST":
#         query = request.POST['query'].strip()
#         if not query:
#             # FIXME Message user that query was empty
#             return render(request, 'rango/search.html', { })

#         context_dict['result_list'] = run_query(query)

#     return render(request, 'rango/search.html', context_dict)

def suggest_category(request):
    if request.method != "GET":
        # FIXME Msg user
        return redirect('/rango/')

    query = request.GET.get('query')
    if not query:
        # FIXME Msg user
        return redirect('/rango/')

    cat_list = get_category_list(8, query)
    return render(request, 'rango/cats.html', { 'cats': cat_list })

def track_url(request):
    if request.method != "GET" or 'page_id' not in request.GET:
        return redirect('/rango/')

    try:
        # This assumes that page_id is an int
        page_id = request.GET.get('page_id')
        page = Page.objects.get(id=page_id)
        page.views += 1
        page.save()

        # FIXME What if page.url cannot be followed?
        return redirect(page.url)
    except Page.DoesNotExist:
        # FIXME Message user
        return redirect('/rango/')

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)

#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('/rango/')
#             else:
#                 return HttpResponse("Your Rango account is disabled. Pfft!")
#         else:
#             err_msg = "Invalid login details: {0}, {1}".format(username, password)
#             print err_msg
#             context_dict = { 'err_msg': err_msg }
#             return render(request, 'rango/login.html', context_dict)
# #             return HttpResponse("Invalid login details supplied.")
#     else:
#         return render(request, 'rango/login.html', { })

# @login_required
# def user_logout(request):
#     logout(request)

#     return redirect('/rango/')
