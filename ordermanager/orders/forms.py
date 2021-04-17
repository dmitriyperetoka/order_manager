from django import forms
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Order, ParameterInOrder, Parameter


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service']

    def __init__(self, data=None, **kwargs):
        self.parameters = None

        if data is not None:
            self.parameters_in_service = dict()
            for q in range(int(data.get('parameters_quantity', 0))):
                title = data[f'parameter_title_{q}']
                value = data[f'parameter_value_{q}']
                self.parameters_in_service[title] = value

        super().__init__(data=data, **kwargs)

    @transaction.atomic
    def save(self, commit=True):
        order = super().save(commit=False)
        order.save()

        parameters_in_order = []
        for title, value in self.parameters_in_service.items():
            parameter = get_object_or_404(Parameter, title=title)
            parameters_in_order.append(
                ParameterInOrder(
                    order=order, parameter=parameter, value=value))
        ParameterInOrder.objects.bulk_create(parameters_in_order)

        self.save_m2m()
        return order


class OrderCompleteForm(forms.ModelForm):
    class Meta:
        fields = ['performer', 'complete']
        model = Order
