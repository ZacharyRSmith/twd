from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from rango.models import Category, Page
import datetime

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

def add_page(title, url, views=0):
    cat = add_cat('test')
    p = Page.objects.get_or_create(category=cat, title=title, url=url,
                                   first_visit=timezone.now(),
                                   last_visit=timezone.now())[0]
#     p.first_visit = timezone.now()
#     p.last_visit = timezone.now()
    p.views = views
    p.save()
    return p


class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """ ensure_views_are_positive expects a category initiated with
            negative views to still have non-negative views after saving
        """
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """ slug_line_creation expects a category to be given an appropriate
            slug. Eg: "Random Category String" -> "random-category-string"
        """
        cat = Category(name="Random Category String")
        cat.save()
        self.assertEqual(cat.slug, "random-category-string")


class IndexViewTests(TestCase):

    def test_index_view_with_categories(self):
        """ If categories exist, expect them to be displayed """
        add_cat('test',1,1)
        add_cat('temp',1,1)
        add_cat('tmp',1,1)
        add_cat('tmp test temp',1,1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'tmp test temp')

        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 4)

    def test_index_view_with_no_categories(self):
        """ If no categories exist, expect a message """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])


class PageMethodTests(TestCase):

    def test_expect_present_first_and_last_visit_to_be_valid(self):
        page = add_page('google', 'http://www.google.com')
        try:
            page.save()
        except ValidationError:
            self.fail('page.save() raised ValidationError unexpectedly!')

    def test_expect_future_last_visit_to_be_invalid(self):
        page = add_page('google', 'http://www.google.com')
        page.last_visit = timezone.now() + datetime.timedelta(days=30)
        self.assertRaises(ValidationError, page.save)

    def test_expect_past_first_visit_to_be_valid(self):
        page = add_page('google', 'http://www.google.com')
        page.first_visit = timezone.now() - datetime.timedelta(days=30)
        try:
            page.save()
        except ValidationError:
            self.fail('page.save() raised ValidationError unexpectedly!')

    def test_expect_last_visit_to_be_invalid_if_in_first_visits_past(self):
        page = add_page('google', 'http://www.google.com')
        page.last_visit = timezone.now() - datetime.timedelta(days=30)
        self.assertRaises(ValidationError, page.save)
