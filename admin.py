from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(DnsKey)
admin.site.register(Zone)
admin.site.register(DynamicDomain)
