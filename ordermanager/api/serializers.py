from rest_framework import serializers

from orders.models import Order, ParameterInOrder


class ParameterInOrderSerializer(serializers.ModelSerializer):
    parameter = serializers.CharField()

    class Meta:
        model = ParameterInOrder
        fields = ['parameter', 'value']
        verbose_name = 'Параметры'


class OrderReadSerializer(serializers.ModelSerializer):
    parameters_assigned = ParameterInOrderSerializer(many=True)
    service = serializers.CharField()

    class Meta:
        model = Order
        fields = ['id', 'service', 'parameters_assigned', 'complete']


class OrderWriteSerializer(serializers.ModelSerializer):
    performer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    complete = serializers.HiddenField(default=True)

    class Meta:
        model = Order
        fields = ['performer', 'complete']
