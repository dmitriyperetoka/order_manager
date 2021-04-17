from django.shortcuts import render


def bad_request(request, exception):  # noqa
    """Handle bad request error."""
    return render(request, 'misc/400.html', status=400)


def permission_denied(request, exception):  # noqa
    """Handle forbidden error."""
    return render(request, 'misc/403.html', status=403)


def page_not_found(request, exception):  # noqa
    """Handle not found error."""
    return render(request, 'misc/404.html', status=404)


def server_error(request):
    """Handle internal server error."""
    return render(request, 'misc/500.html', status=500)
