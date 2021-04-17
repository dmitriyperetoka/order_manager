from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Order, ParameterInOrder, ServiceParameter


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service']

    def __init__(self, data=None, **kwargs):
        self.parameter_titles = None
        self.parameter_values = None

        if data is not None:
            self.parameter_titles = data.getlist('parameter_title')
            self.parameter_values = data.getlist('parameter_value')
        super().__init__(data=data, **kwargs)

    def clean(self):
        exception = ValidationError(
            'Заполните все значения параметров услуги для заказа.')

        if len(self.parameter_titles) != len(self.parameter_values):
            raise exception

        for value in self.parameter_values:
            if not value:
                raise exception

        return super().clean()

    @transaction.atomic
    def save(self, commit=True):
        order = super().save(commit=False)
        order.save()

        parameters = []
        for title, value in zip(self.parameter_titles, self.parameter_values):
            parameter = get_object_or_404(ServiceParameter, title=title)
            parameters.append(
                ParameterInOrder(
                    order=order, parameter=parameter, value=value))
        ParameterInOrder.objects.bulk_create(parameters)

        self.save_m2m()
        return order
