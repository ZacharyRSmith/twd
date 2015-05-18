from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^categories/$', views.category_index, name='category_index'),
    url(r'^category_index/$', views.category_index, name='category_index'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^home/$', views.index, name='index'),
    url(r'^homepage/$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^restricted/$', views.restricted, name='restricted'),
)