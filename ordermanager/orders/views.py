from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DetailView, ListView, RedirectView, UpdateView,
)

from .forms import OrderCompleteForm, OrderCreateForm
from .mixins import IsNotStaffPermissionMixin, IsStaffPermissionMixin
from .models import Order, Service


class ServiceListView(IsNotStaffPermissionMixin, ListView):
    """Display list of services."""
    model = Service


class OrderCreateView(IsNotStaffPermissionMixin, CreateView):
    """Create new orders."""

    success_url = reverse_lazy('orders:index')
    form_class = OrderCreateForm
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = get_object_or_404(Service, id=self.kwargs['service_id'])
        context['service'] = service
        context['parameters_in_service'] = (
            service.parameters_assigned.select_related('parameter'))
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class OrderListView(IsStaffPermissionMixin, ListView):
    """Display list of orders that have not been done yet."""
    queryset = Order.objects.filter(complete=False).select_related('service')


class OrderDetailView(IsStaffPermissionMixin, DetailView):
    """Display details of an order."""
    model = Order


class OrderCompleteView(IsStaffPermissionMixin, UpdateView):
    """Complete an order."""
    form_class = OrderCompleteForm
    model = Order

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        if self.object.complete is not True:
            self.object.complete = True
            self.object.performer = self.request.user
            self.object.save()

        return HttpResponseRedirect(
            reverse('orders:order_detail', kwargs={'pk': self.object.id}))


class RouteView(LoginRequiredMixin, RedirectView):
    """Redirect staff and non-staff users to different pages."""

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_staff:
            return reverse('orders:order_list')
        return reverse('orders:services_list')
