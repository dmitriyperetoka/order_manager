from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import OrderForm
from .models import Order, Service


class ServiceListView(ListView):
    model = Service


class OrderCreateView(CreateView):
    success_url = reverse_lazy('orders:index')
    form_class = OrderForm
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
