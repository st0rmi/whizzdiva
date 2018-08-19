# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from whizzdiva.forms import DynamicDomainForm
from whizzdiva.models import DynamicDomain


def index(request):
    return HttpResponse("Hello, world.") # TODO: default landing page


class DynamicDomainsOverview(LoginRequiredMixin, generic.ListView):
    template_name = 'whizzdiva/dynamic_domains_overview.html'
    context_object_name = 'dynamic_domains'

    def get_queryset(self):
        return DynamicDomain.objects.order_by('zone__domain', 'relative_domain')


class DynamicDomainView(LoginRequiredMixin, generic.DetailView):
    model = DynamicDomain
    template_name = 'whizzdiva/dynamic_domain_details.html'


@login_required
def add_dynamic_domain(request):
    if request.method == 'POST':
        form = DynamicDomainForm(request.POST)
        if form.is_valid():
            dynamic_domain = form.save(commit=False)
            dynamic_domain.owner = request.user
            dynamic_domain.save()
            return HttpResponseRedirect(reverse('whizzdiva:dynamic_domain_details', args=(dynamic_domain.pk,)))
    else:
        form = DynamicDomainForm()
    return render(request, "whizzdiva/dynamic_domain_add_edit.html", {'form' : form})
