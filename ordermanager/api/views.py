from django.contrib.auth import get_user_model
from rest_framework import mixins, permissions, viewsets

from .permissions import IsStaffPermission
from .serializers import OrderReadSerializer, OrderWriteSerializer
from orders.models import Order

User = get_user_model()


class OrderListRetrieveUpdateViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated, IsStaffPermission]
    queryset = Order.objects.filter(complete=False).select_related('service')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderReadSerializer
        return OrderWriteSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Order.objects.filter(
                complete=False).select_related('service')
        return Order.objects.select_related('service')
