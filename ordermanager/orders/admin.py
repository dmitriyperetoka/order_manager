from django.contrib import admin

from .models import (
    Order, ParameterInOrder, Service, ServiceParameter,
    ServiceParameterInService,
)

admin.site.register(Order)
admin.site.register(ParameterInOrder)
admin.site.register(Service)
admin.site.register(ServiceParameter)
admin.site.register(ServiceParameterInService)
