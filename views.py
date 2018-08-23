# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from whizzdiva.forms import DynamicDomainForm
from whizzdiva.models import DynamicDomain


def index(request):
    return render(request, "whizzdiva/index.html")


class DynamicDomainsOverview(LoginRequiredMixin, generic.ListView):
    template_name = 'whizzdiva/dynamic_domains_overview.html'
    context_object_name = 'dynamic_domains'

    def get_queryset(self):
        return DynamicDomain.objects.order_by('zone__domain', 'relative_domain').filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['add_form'] = DynamicDomainForm()
        return context


class DynamicDomainView(LoginRequiredMixin, generic.DetailView):
    model = DynamicDomain
    template_name = 'whizzdiva/dynamic_domain_details.html'

    def get_queryset(self):
        return super(DynamicDomainView, self).get_queryset().filter(owner=self.request.user)


@login_required
def add_dynamic_domain(request):
    if request.method == 'POST':
        form = DynamicDomainForm(request.POST)
        if form.is_valid():
            dynamic_domain = form.save(commit=False)
            dynamic_domain.owner = request.user
            dynamic_domain.save()
            return HttpResponseRedirect(reverse('whizzdiva:dynamic_domains_overview'))
    else:
        form = DynamicDomainForm()

    return render(request, "whizzdiva/dynamic_domain_add_edit.html", {'form': form, 'add': True})


@login_required
def edit_dynamic_domain(request, pk):
    dynamic_domain = get_object_or_404(DynamicDomain, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = DynamicDomainForm(request.POST or None, instance=dynamic_domain)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('whizzdiva:dynamic_domains_overview'))
    else:
        form = DynamicDomainForm(instance=dynamic_domain)

    return render(request, "whizzdiva/dynamic_domain_add_edit.html", {'form': form})


@login_required
def delete_dynamic_domain(request, pk):
    dynamic_domain = get_object_or_404(DynamicDomain, pk=pk, owner=request.user)

    if request.method == 'POST':
        dynamic_domain.delete()
        return HttpResponseRedirect(reverse('whizzdiva:dynamic_domains_overview'))
    else:
        return render(request, "whizzdiva/dynamic_domain_delete.html", {'dynamic_domain': dynamic_domain})
