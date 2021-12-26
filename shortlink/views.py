from datetime import datetime
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse

from django.views.generic.edit import UpdateView

from .models import Link, Domain

from .forms import LinkForm, DomainForm, UTMForm, ContactForm

from .slug import Slug

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

import pyperclip
import urllib

from django.core.mail import send_mail
from django.conf import settings


@login_required
def index(request):
    if request.method == 'POST':
        form = LinkForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data['title']
            source_link = form.cleaned_data['source_link']
            user_slug = form.cleaned_data['slug']
            domain = form.cleaned_data['domain']

            slug = user_slug if user_slug else Slug.slug()
            slug = str(domain) + '/' + str(slug) if domain else slug

            while True:

                if not Link.objects.filter(slug=slug).exists():

                    try:
                        link = Link(user=user, title=title, source_link=source_link, slug=slug)
                        link.save()
                        break

                    except IntegrityError:
                        pass
                else:
                    messages.warning(request, 'This combination of Domain and Slug already exists!')
                    break

            return HttpResponseRedirect(reverse('shortlink:index', args=None))
    else:
       form = LinkForm(request.user)
    my_links_list = Link.objects.filter(user=request.user).order_by('-date_modified')
    context = {'form': form, 'my_links_list': my_links_list}

    return render(request, 'shortlink/index.html', context)


@login_required
def manage_domains(request):
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            user = request.user
            domain_name = form.cleaned_data['domain_name']

            if not Domain.objects.filter(domain_name=domain_name).exists():

                try:
                    domain = Domain(user=user, domain_name=domain_name)
                    domain.save()

                except IntegrityError:
                    pass

            return HttpResponseRedirect(reverse('shortlink:manage_domains', args=None))
    else:
       form = DomainForm()
    my_domains_list = Domain.objects.filter(user=request.user).order_by('date_created')
    context = {'form': form, 'my_domains_list': my_domains_list}

    return render(request, 'shortlink/manage_domains.html', context)


@login_required
def create_utm(request):
    if request.method == 'POST':
        form = UTMForm(request.POST)
        if form.is_valid():
            homepage = form.cleaned_data['homepage']
            utm_source = form.cleaned_data['utm_source']
            utm_medium = form.cleaned_data['utm_medium']
            utm_campaign = form.cleaned_data['utm_campaign']
            utm_content = form.cleaned_data['utm_content']
            utm_term = form.cleaned_data['utm_term']

            utm_url_dict = {'utm_source': utm_source,
                            'utm_medium': utm_medium,
                            'utm_campaign': utm_campaign
                            }

            if utm_content:
                utm_url_dict['utm_content'] = utm_content

            if utm_term:
                utm_url_dict['utm_term'] = utm_term

            utm_url = homepage + '/?' + urllib.parse.urlencode(utm_url_dict)
            pyperclip.copy(utm_url)
            messages.success(request, 'UTM link created and copied to clipboard!')

            context = {'form': form, 'utm_url': utm_url}

            return render(request, 'shortlink/create_utm.html', context)
    else:
        form = UTMForm()
    context = {'form': form}
    return render(request, 'shortlink/create_utm.html', context)


@login_required
def delete_domain(request, domain_id):
    if request.method == "POST":
        domain_to_delete = Domain.objects.get(id=domain_id)
        domain_to_delete.delete()
    return redirect(reverse('shortlink:manage_domains'))


@login_required
def to_the_top(request, link_id):
    if request.method == "POST":
        link_to_the_top = Link.objects.get(id=link_id)
        link_to_the_top.date_modified = datetime.now()
        link_to_the_top.save()
    return redirect(reverse('shortlink:index'))


@login_required
def delete_link(request, link_id):
    if request.method == "POST":
        link_to_delete = Link.objects.get(id=link_id)
        link_to_delete.delete()
    return redirect(reverse('shortlink:index'))


@method_decorator(login_required, name='dispatch')
class EditLinkView(UpdateView):

    def post(self, request, *args, **kwargs):

        super().post(request)
        form = self.get_form()
        if form.is_valid():
            messages.success(request, 'Link updated!')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    model = Link
    fields = ['title', 'source_link']
    template_name_suffix = '_update_form'


def link_redirect(request, link_slug1, link_slug2=None):
    if request.method == 'GET':
        requested_url = link_slug1 if not link_slug2 else link_slug1 + '/' + link_slug2
        if Link.objects.filter(slug=requested_url).exists():
            link_to_redirect = Link.objects.get(slug=requested_url)
            return HttpResponseRedirect(str(link_to_redirect))
        else:
            raise Http404('Link does not exists.')


def about_the_project(request):
    return render(request, 'shortlink/about_the_project.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_text = form.cleaned_data['message_text']
            result_message = 'User ' + name + ' email: ' + email + ' sent a message:' + '\n\n' + message_text

            send_mail(
                subject,
                result_message,
                settings.EMAIL_HOST_USER,
                ['drdizel@mail.ru'],
                fail_silently=False,
            )
            context = {'form': form}
            messages.success(request, 'Message is sent. We will response you soon.')
            return render(request, 'shortlink/contact_us.html', context)
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request, 'shortlink/contact_us.html', context)


def terms_of_use(request):
    return render(request, 'shortlink/terms_of_use.html')


def privacy_policy(request):
    return render(request, 'shortlink/privacy_policy.html')
