from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path(
        'order/<int:service_id>/', views.OrderCreateView.as_view(),
        name='order_create'),
    path(
        'order/success/', views.OrderCreateSuccessView.as_view(),
        name='order_create_success'),
    path('', views.ServiceListView.as_view(), name='index'),
]
