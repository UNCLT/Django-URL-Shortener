from django.contrib import admin

from .models import Link, Domain, SecureLink
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class LinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'source_link', 'slug', 'date_created', 'date_modified']
    ordering = ['-date_modified']


class SecureLinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'openings_number', 'open_counter', 'date_created']
    ordering = ['-date_created']


class DomainAdmin(admin.ModelAdmin):
    list_display = ['user', 'domain_name', 'date_created']
    ordering = ['-date_created']


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    ordering = ['-date_joined']


admin.site.register(Link, LinkAdmin)
admin.site.register(SecureLink, SecureLinkAdmin)
admin.site.register(Domain, DomainAdmin)
