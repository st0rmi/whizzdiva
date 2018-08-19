from django.core.exceptions import NON_FIELD_ERRORS
from django.forms import ModelForm

from whizzdiva.models import DynamicDomain


class DynamicDomainForm(ModelForm):
    class Meta:
        model = DynamicDomain
        fields = ['zone', 'relative_domain']

        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(relative_domain)s.%(zone.domain)s is already taken.",
            }
        }