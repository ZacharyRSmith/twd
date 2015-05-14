from django import forms
from rango.models import Category, Page


class CategoryForm(forms.ModelForm):
    name  = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug  = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url   = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)
        #fields = ('title', 'url', 'views',)

    def clean(self):
        c_data = self.cleaned_data
        url = c_data.get('url')

        if url and not url.startswith('http://'):
            if not url.startswith('www.'):
                url = 'http://www.' + url
            else:
                url = 'http://' + url

        c_data['url'] = url
        return c_data
