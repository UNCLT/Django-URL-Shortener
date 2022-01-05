from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')


class Domain(models.Model):

    domain_name = models.CharField('Name of domain', max_length=10, unique=True, validators=[alphanumeric])
    date_created = models.DateTimeField('Date of creation', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.domain_name


class Link(models.Model):

    title = models.CharField('Title', max_length=200, blank=True)
    description = models.TextField('Description', max_length=500, blank=True)
    source_link = models.URLField('Source link', max_length=2000)
    date_created = models.DateTimeField('Date of creation', auto_now_add=True)
    date_modified = models.DateTimeField('Date of modification', auto_now=True)
    slug = models.CharField('Slug', max_length=15, blank=True, validators=[alphanumeric])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.source_link

    def get_absolute_url(self):
        return reverse('shortlink:edit_link', kwargs={'pk': self.pk})


class SecureLink(models.Model):

    date_created = models.DateTimeField('Date of creation', auto_now_add=True)
    data = models.TextField('Text to secure', blank=False)
    openings_number = models.PositiveIntegerField('Openings number')
    open_counter = models.PositiveIntegerField('Counter of openings', default=0)
    slug = models.CharField('Slug', max_length=20, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.slug
