from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('services/<int:service_id>/order/', views.OrderCreateView.as_view(),
         name='order_create'),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('orders/<int:pk>/complete', views.OrderCompleteView.as_view(),
         name='order_complete'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(),
         name='order_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('', views.RouteView.as_view(), name='index'),
]
