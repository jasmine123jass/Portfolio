from django.shortcuts import render
from django.http import HttpResponseServerError, HttpResponseNotFound


def custom_404(request, exception=None):
    """Simple 404 handler used by urls.handler404.

    Renders `404.html` if present, otherwise returns a plain HttpResponseNotFound.
    """
    try:
        return render(request, '404.html', status=404)
    except Exception:
        return HttpResponseNotFound('404 Not Found')


def custom_500(request):
    """Simple 500 handler used by urls.handler500.

    Renders `500.html` if present, otherwise returns a plain HttpResponseServerError.
    """
    try:
        return render(request, '500.html', status=500)
    except Exception:
        return HttpResponseServerError('500 Internal Server Error')
