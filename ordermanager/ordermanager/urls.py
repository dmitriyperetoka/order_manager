from django.conf.urls import (  # noqa
    handler400, handler403, handler404, handler500
)
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

handler400 = 'ordermanager.views.bad_request'  # noqa
handler403 = 'ordermanager.views.permission_denied'  # noqa
handler404 = 'ordermanager.views.page_not_found'  # noqa
handler500 = 'ordermanager.views.server_error'  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('orders.urls', namespace='orders')),
]
