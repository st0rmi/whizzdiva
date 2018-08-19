# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic

from whizzdiva.models import DynamicDomain


def index(request):
    return HttpResponse("Hello, world.")


class DynamicDomainsOverview(LoginRequiredMixin, generic.ListView):
    template_name = 'whizzdiva/dynamic_domains_overview.html'
    context_object_name = 'dynamic_domains'

    def get_queryset(self):
        return DynamicDomain.objects.order_by('zone__domain', 'relative_domain')


class DynamicDomainView(LoginRequiredMixin, generic.DetailView):
    model = DynamicDomain
    template_name = 'whizzdiva/dynamic_domain_details.html'
