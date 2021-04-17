from django import forms
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Order, ParameterInOrder, ServiceParameter


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service']

    def __init__(self, data=None, **kwargs):
        self.parameters = None

        if data is not None:
            print('\n', data, '\n')
            self.parameters_in_service = dict()
            for q in range(int(data.get('parameters_quantity', 0))):
                title = data[f'parameter_title_{q}']
                value = data[f'parameter_value_{q}']
                self.parameters_in_service[title] = value
            print('\n', self.parameters_in_service, '\n')

        super().__init__(data=data, **kwargs)

    @transaction.atomic
    def save(self, commit=True):
        order = super().save(commit=False)
        order.save()
        print('\n', order, '\n')

        parameters_in_order = []
        for title, value in self.parameters_in_service.items():
            parameter = get_object_or_404(ServiceParameter, title=title)
            parameters_in_order.append(
                ParameterInOrder(
                    order=order, parameter=parameter, value=value))
        print(parameters_in_order)
        ParameterInOrder.objects.bulk_create(parameters_in_order)

        self.save_m2m()
        return order
