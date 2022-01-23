from django.urls import path
from . import views
from .views import EditLinkView

app_name = 'shortlink'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:link_id>/to_the_top', views.to_the_top, name='to_the_top'),
    path('<int:link_id>/delete_link', views.delete_link, name='delete_link'),
    path('<int:pk>/edit_link', EditLinkView.as_view(), name='edit_link'),
    path('manage_domains/', views.manage_domains, name='manage_domains'),
    path('<int:domain_id>/delete_domain', views.delete_domain, name='delete_domain'),
    path('create_utm/', views.create_utm, name='create_utm'),
    path('about_the_project/', views.about_the_project, name='about_the_project'),
    path('contact_us/', views.contact_us, name='contact_us'),

    path('create_secure_link/', views.create_secure_link, name='create_secure_link'),

    path('<str:link_slug1>', views.link_redirect, name='link_redirect'),
    path('<str:link_slug1>/<str:link_slug2>/', views.link_redirect, name='link_redirect'),

    path('terms_of_use/', views.terms_of_use, name='terms_of_use'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy')
]
