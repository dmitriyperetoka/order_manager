from django.contrib import admin

from .models import (
    Order, ParameterInOrder, Service, Parameter,
    ParameterInService,
)

admin.site.register(Order)
admin.site.register(ParameterInOrder)
admin.site.register(Service)
admin.site.register(Parameter)
admin.site.register(ParameterInService)
