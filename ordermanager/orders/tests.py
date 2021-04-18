from django.contrib.auth import get_user_model
from orders.models import Order, Service
from django.shortcuts import reverse
from django.test import TestCase

User = get_user_model()


class BaseSetUp(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='someuser', is_staff=True)
        self.another_user = User.objects.create(username='anotheruser')
        self.client.force_login(self.user)
        self.service = Service.objects.create()
        self.order = Order.objects.create(service=self.service)


class UrlsTestBase(TestCase):
    def check_exists(self, urls):
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def check_forbidden(self, urls):
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

    def check_redirects(self, redirects):
        for url, redirect_url in redirects.items():
            with self.subTest():
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)


class ViewsTestBase(TestCase):
    def check_template_used(self, reverse_names_templates):
        for reverse_name, template in reverse_names_templates:
            with self.subTest():
                response = self.client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def check_object_in_context(self, pages):
        for path, obj in pages:
            response = self.client.get(path)
            with self.subTest():
                self.assertEqual(response.context['object'], obj)

    def check_object_list_in_context(self, pages):
        for path, queryset in pages:
            response = self.client.get(path)
            with self.subTest():
                self.assertQuerysetEqual(
                    response.context['object_list'], map(repr, queryset))


class OrdersUrlsTest(UrlsTestBase, BaseSetUp):
    def test_exists(self):
        urls = [
            '/orders/',
            f'/orders/{self.order.id}/',
            f'/orders/{self.order.id}/complete',
        ]
        self.check_exists(urls)

        self.client.force_login(self.another_user)
        urls = [
            '/services/',
            f'/services/{self.order.id}/order/',
        ]
        self.check_exists(urls)

    def test_forbidden(self):
        urls = [
            '/services/',
            f'/services/{self.order.id}/order/',
        ]
        self.check_forbidden(urls)

        self.client.force_login(self.another_user)
        urls = [
            '/orders/',
            f'/orders/{self.order.id}/',
            f'/orders/{self.order.id}/complete',
        ]
        self.check_forbidden(urls)

    def test_redirects(self):
        redirects = {'/': '/orders/'}
        self.check_redirects(redirects)

        self.client.force_login(self.another_user)
        redirects = {'/': '/services/'}
        self.check_redirects(redirects)


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
        pages = [(reverse('orders:order_list'), order_queryset)]
        self.check_object_list_in_context(pages)

        self.client.force_login(self.another_user)
        service_queryset = Service.objects.all()
        pages = [(reverse('orders:service_list'), service_queryset)]
        self.check_object_list_in_context(pages)
