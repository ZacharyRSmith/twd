from django.core.urlresolvers import reverse
from django.test import TestCase
from rango.models import Category

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


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
