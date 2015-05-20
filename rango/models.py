from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone


class Category(models.Model):
    likes = models.IntegerField(default=0)
    name  = models.CharField(max_length=128, unique=True)
    slug  = models.SlugField(unique=True)
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.views >= 0:
            self.views = 0
        super(Category, self).save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username


class Page(models.Model):
    category = models.ForeignKey(Category)
    first_visit = models.DateTimeField('Time of first visit. #BigBrother')
    last_visit = models.DateTimeField('Time of last visit. #BigBrother')
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.first_visit > timezone.now():
            raise ValidationError('first_visit cannot be in the future!')

        if self.last_visit > timezone.now():
            raise ValidationError('last_visit cannot be in the future!')

        if self.last_visit < self.first_visit:
            raise ValidationError('last_visit cannot be in first_visit\'s past!')

        super(Page, self).save(*args, **kwargs)
