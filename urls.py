from django.urls import path

from . import views

app_name = 'whizzdiva'
urlpatterns = [
    path('', views.index, name='index'),
    path('dynamic_domain/', views.DynamicDomainsOverview.as_view(), name='dynamic_domains_overview'),
    path('dynamic_domain/add/', views.add_dynamic_domain, name='dynamic_domain_add'),
    path('dynamic_domain/<int:pk>/', views.DynamicDomainView.as_view(), name='dynamic_domain_details'),
    path('dynamic_domain/<int:pk>/edit/', views.edit_dynamic_domain, name='dynamic_domain_edit'),
    path('dynamic_domain/<int:pk>/delete/', views.delete_dynamic_domain, name='dynamic_domain_delete'),
]
