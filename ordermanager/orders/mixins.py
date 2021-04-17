from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin,
)


class OrdersBasePermissionMixin(LoginRequiredMixin, PermissionRequiredMixin):
    pass


class IsStaffPermissionMixin(OrdersBasePermissionMixin):
    def has_permission(self):
        user = self.request.user  # noqa
        return user.is_superuser or user.is_staff


class IsNotStaffPermissionMixin(OrdersBasePermissionMixin):
    def has_permission(self):
        user = self.request.user  # noqa
        return user.is_superuser or not user.is_staff
