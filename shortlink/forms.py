from django import forms

from .models import Link, Domain


class LinkForm(forms.ModelForm):
    title = forms.CharField(label='Title (optional)', max_length=200, required=False)
    source_link = forms.URLField(label='URL to shorten', max_length=2000)
    slug = forms.CharField(label='Slug (optional) ya.link/YOUR_SLUG', max_length=50, required=False)

    class Meta:
        model = Link
        fields = ['title', 'source_link', 'slug']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['domain'] = forms.ModelChoiceField(label='Domain (optional)', queryset=Domain.objects.filter(user=user), required=False)


class DomainForm(forms.ModelForm):
    domain_name = forms.CharField(label='Name of domain', max_length=10, required=True)

    class Meta:
        model = Domain
        fields = ['domain_name']


class UTMForm(forms.Form):
    homepage = forms.URLField(label='Website URL (http://www.mysite.com)', max_length=100, required=True)
    utm_source = forms.CharField(label='Campaign Source (utm_source)', max_length=50, required=True)
    utm_medium = forms.CharField(label='Campaign Medium (utm_medium)', max_length=50, required=True)
    utm_campaign = forms.CharField(label='Campaign Name (utm_campaign)', max_length=50, required=True)
    utm_content = forms.CharField(label='Campaign Content (utm_content)', max_length=50, required=False)
    utm_term = forms.CharField(label='Campaign Term (utm_term)', max_length=50, required=False)


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50, required=True)
    email = forms.EmailField(label='Email', max_length=50, required=True)
    subject = forms.CharField(label='Subject', max_length=100, required=False)
    message_text = forms.CharField(widget=forms.Textarea, label='Your message', max_length=3000, required=True)
