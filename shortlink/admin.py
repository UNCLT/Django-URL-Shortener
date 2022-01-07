from django.contrib import admin

from .models import Link, Domain


class LinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'source_link', 'slug', 'date_created', 'date_modified']
    ordering = ['-date_modified']


class DomainAdmin(admin.ModelAdmin):
    list_display = ['user', 'domain_name', 'date_created']
    ordering = ['-date_created']


admin.site.register(Link, LinkAdmin)
admin.site.register(Domain, DomainAdmin)
