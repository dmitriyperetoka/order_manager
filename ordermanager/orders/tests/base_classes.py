from django.contrib.auth import get_user_model
from django.test import TestCase

from orders.models import Order, Service

User = get_user_model()


class ModelsTestBase(TestCase):
    def check_field_list(self, instance, field_names, many_to_many=False):
        instance_fields = (
            instance._meta.many_to_many
            if many_to_many else instance._meta.fields)
        instance_field_names = [q.name for q in instance_fields]
        self.assertListEqual(instance_field_names, field_names)

    def check_field_classes(self, instance, field_classes):
        for field, _class in field_classes.items():
            with self.subTest():
                self.assertIsInstance(instance._meta.get_field(field), _class)

    def check_cascade(self, model, foreign_key, foreign_model, fm_instance):
        instance = model.objects.filter(**{foreign_key: fm_instance})
        with self.subTest():
            self.assertTrue(instance.exists())
        foreign_model.objects.get(id=fm_instance.id).delete()
        self.assertFalse(instance.exists())

    def check_related_names(self, instance, relations, one_to_one=False):
        for related_instance, related_name in relations:
            with self.subTest():
                if one_to_one:
                    query = related_instance.__getattribute__(related_name)
                    self.assertEqual(instance, query)
                else:
                    query = (
                        related_instance.__getattribute__(related_name).all())
                    self.assertIn(instance, query)

    def check_field_attrs(self, instance, field_attrs, remote=False):
        for field, attrs in field_attrs.items():
            for attr, value in attrs.items():
                with self.subTest():
                    instance_field = (
                        instance._meta.get_field(field).remote_field
                        if remote else instance._meta.get_field(field))
                    self.assertEqual(
                        instance_field.__getattribute__(attr), value)

    def check_model_attrs(self, instance, model_attrs):
        for attr, attr_value in model_attrs.items():
            with self.subTest():
                self.assertEqual(
                    instance._meta.__getattribute__(attr), attr_value)


class UrlsTestBase(TestCase):
    def check_exists(self, urls):
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def check_redirects(self, redirects, remote=False):
        for url, redirect_url in redirects.items():
            with self.subTest():
                response = self.client.get(url)
                self.assertRedirects(
                    response, redirect_url,
                    fetch_redirect_response=False if remote else True)

    def check_redirect_chains(self, redirect_chains):
        for url, chain in redirect_chains.items():
            with self.subTest():
                response = self.client.get(url, follow=True)
                self.assertEqual(response.redirect_chain, chain)

    def check_unauthorized_forbidden(self, urls):
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, 403)

    def check_get_method_not_allowed(self, urls):
        for url in urls:
            with self.subTest():
                response = self.client.get(url)
                self.assertEqual(response.status_code, 405)


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


class BaseSetUp(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='someuser', is_staff=True)
        self.another_user = User.objects.create(username='anotheruser')
        self.client.force_login(self.user)
        self.service = Service.objects.create()
        self.order = Order.objects.create(service=self.service)
