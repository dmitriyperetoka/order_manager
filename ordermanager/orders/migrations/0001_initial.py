# Generated by Django 3.2 on 2021-04-17 23:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('complete', models.BooleanField(db_index=True, default=False, verbose_name='Выполнено')),
                ('author', models.ForeignKey(help_text='Автор заказа', limit_choices_to=models.Q(is_staff=False), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders_issued', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('performer', models.ForeignKey(help_text='Исполнитель заказа', limit_choices_to=models.Q(is_staff=True), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders_performed', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['time_created'],
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Наименование параметра услуги', max_length=200, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Параметр услуги',
                'verbose_name_plural': 'Параметры услуг',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Наименование услуги', max_length=200, unique=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ParameterInService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('checkbox', 'Чекбокс'), ('text', 'Текст'), ('number', 'Целое число')], help_text='Тип поля формы', max_length=8, verbose_name='Тип')),
                ('parameter', models.ForeignKey(help_text='Параметр, который задан для услуги', on_delete=django.db.models.deletion.CASCADE, related_name='services_assigned', to='orders.parameter', verbose_name='Параметр')),
                ('service', models.ForeignKey(help_text='Услуга, для которой задан параметр', on_delete=django.db.models.deletion.CASCADE, related_name='parameters_assigned', to='orders.service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Тип параметра для услуги',
                'verbose_name_plural': 'Типы параметров для услуг',
                'ordering': ['type', 'parameter'],
            },
        ),
        migrations.CreateModel(
            name='ParameterInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(help_text='Значение параметра услуги в заказе', max_length=2000, verbose_name='Значение')),
                ('order', models.ForeignKey(help_text='Заказ, в котором задан параметр услуги', on_delete=django.db.models.deletion.CASCADE, related_name='parameters_assigned', to='orders.order', verbose_name='Заказ')),
                ('parameter', models.ForeignKey(help_text='Параметр услуги, который задан в заказе', on_delete=django.db.models.deletion.CASCADE, related_name='orders_assigned', to='orders.parameter', verbose_name='Параметр')),
            ],
            options={
                'verbose_name': 'Параметр услуги в заказе',
                'verbose_name_plural': 'Параметры услуг в заказах',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='service',
            field=models.ForeignKey(help_text='Заказываемая услуга', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='orders.service', verbose_name='Услуга'),
        ),
        migrations.AddConstraint(
            model_name='parameterinservice',
            constraint=models.UniqueConstraint(fields=('service', 'parameter'), name='unique_parameter_in_service'),
        ),
        migrations.AddConstraint(
            model_name='parameterinorder',
            constraint=models.UniqueConstraint(fields=('order', 'parameter'), name='unique_parameter_in_order'),
        ),
    ]
