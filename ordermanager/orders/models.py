from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Parameter(models.Model):
    title = models.CharField(
        max_length=200, unique=True, verbose_name='Наименование',
        help_text='Наименование параметра услуги')

    class Meta:
        ordering = ['title']
        verbose_name = 'Параметр услуги'
        verbose_name_plural = 'Параметры услуг'

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(
        max_length=200, unique=True, verbose_name='Наименование',
        help_text='Наименование услуги')

    class Meta:
        ordering = ['title']
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.title


class ParameterInService(models.Model):
    TYPE_CHOICES = [
        ('checkbox', 'Чекбокс'),
        ('text', 'Текст'),
        ('number', 'Целое число'),
    ]
    service = models.ForeignKey(
        Service, models.CASCADE, related_name='parameters_assigned',
        verbose_name='Услуга', help_text='Услуга, для которой задан параметр')
    parameter = models.ForeignKey(
        Parameter, models.CASCADE,
        related_name='services_assigned', verbose_name='Параметр',
        help_text='Параметр, который задан для услуги')
    type = models.CharField(
        max_length=len(max(TYPE_CHOICES, key=lambda x: len(x[0]))[0]),
        choices=TYPE_CHOICES, verbose_name='Тип', help_text='Тип поля формы')

    class Meta:
        ordering = ['type', 'parameter']
        verbose_name = 'Тип параметра для услуги'
        verbose_name_plural = 'Типы параметров для услуг'
        constraints = [
            models.UniqueConstraint(
                fields=['service', 'parameter'],
                name='unique_parameter_in_service',
            ),
        ]

    def __str__(self):
        return (
            f'Для услуги "{self.service}" задан параметр "{self.parameter}" '
            f'с типом "{self.type}"')


class Order(models.Model):
    author = models.ForeignKey(
        User, models.SET_NULL, null=True, related_name='orders_issued',
        verbose_name='Автор', help_text='Автор заказа',
        limit_choices_to=models.Q(is_staff=False))
    service = models.ForeignKey(
        Service, models.CASCADE, related_name='orders', verbose_name='Услуга',
        help_text='Заказываемая услуга')
    time_created = models.DateTimeField(auto_now_add=True, db_index=True)
    complete = models.BooleanField(
        verbose_name='Выполнено', default=False, db_index=True)
    performer = models.ForeignKey(
        User, models.SET_NULL, null=True, related_name='orders_performed',
        verbose_name='Исполнитель', help_text='Исполнитель заказа',
        limit_choices_to=models.Q(is_staff=True))

    class Meta:
        ordering = ['time_created']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ #{self.id} {self.service.title}'


class ParameterInOrder(models.Model):
    order = models.ForeignKey(
        Order, models.CASCADE,
        related_name='parameters_assigned', verbose_name='Заказ',
        help_text='Заказ, в котором задан параметр услуги')
    parameter = models.ForeignKey(
        Parameter, models.CASCADE,
        related_name='orders_assigned', verbose_name='Параметр',
        help_text='Параметр услуги, который задан в заказе')
    value = models.TextField(
        max_length=2000, verbose_name='Значение',
        help_text='Значение параметра услуги в заказе')

    class Meta:
        verbose_name = 'Параметр услуги в заказе'
        verbose_name_plural = 'Параметры услуг в заказах'
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'parameter'],
                name='unique_parameter_in_order',
            ),
        ]

    def __str__(self):
        return f'Параметр {self.parameter} в заказе {str(self.order)[6:]}'
