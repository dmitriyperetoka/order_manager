from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    'orders', views.OrderListRetrieveUpdateViewSet, basename='orders')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
