from django.contrib.auth import get_user_model
from django.shortcuts import reverse

from .base_classes import BaseSetUp, ViewsTestBase
from orders.models import Order, Service

User = get_user_model()


class OrdersViewsTest(ViewsTestBase, BaseSetUp):
    def test_template_used(self):
        reverse_names_templates = [
            (reverse('orders:order_list'), 'orders/order_list.html'),
            (
                reverse(
                    'orders:order_detail', kwargs={'pk': self.order.id}),
                'orders/order_detail.html',
            ),
            (
                reverse(
                    'orders:order_complete', kwargs={'pk': self.order.id}),
                'orders/order_form.html',
            ),
        ]
        self.check_template_used(reverse_names_templates)

        self.client.force_login(self.another_user)
        reverse_names_templates = [
            (
                reverse(
                    'orders:order_create',
                    kwargs={'service_id': self.service.id},
                ),
                'orders/order_form.html'
            ),
            (
                reverse('orders:service_list'),
                'orders/service_list.html',
            ),
        ]
        self.check_template_used(reverse_names_templates)

    def test_object_in_context(self):
        pages = [
            (
                reverse(
                    'orders:order_detail', kwargs={'pk': self.order.id}),
                self.order,
            ),
            (
                reverse(
                    'orders:order_complete', kwargs={'pk': self.order.id}),
                self.order,
            ),
        ]
        self.check_object_in_context(pages)

    def test_object_list_in_context(self):
        order_queryset = Order.objects.all()
        pages = [
            (reverse('orders:order_list'), order_queryset),
        ]
        self.check_object_list_in_context(pages)

        self.client.force_login(self.another_user)
        service_queryset = Service.objects.all()
        pages = [
            (reverse('orders:service_list'), service_queryset),
        ]
        self.check_object_list_in_context(pages)

    def test_extra_context_passed(self):
        pages = [
            (
                reverse(
                    'orders:order_create',
                    kwargs={'service_id': self.service.id}),
                {'service': self.service},
            ),
        ]
        self.check_extra_context_passed(pages)
