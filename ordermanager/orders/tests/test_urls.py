from django.contrib.auth import get_user_model

from .base_classes import BaseSetUp, UrlsTestBase

User = get_user_model()


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

    def test_redirects(self):
        redirects = {'/': '/orders/'}
        self.check_redirects(redirects)

        self.client.force_login(self.another_user)
        redirects = {'/': '/services/'}
        self.check_redirects(redirects)
