from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'dynamicdns'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.login, {'template_name': 'dynamicdns/login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    path('dynamic_domain/', views.DynamicDomainsOverview.as_view(), name='dynamic_domains_overview'),
    path('dynamic_domain/<int:dynamic_domain_id>/', views.DynamicDomainView.as_view(), name='dynamic_domain_details'),
]
