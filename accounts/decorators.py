
from django.core.exceptions import PermissionDenied

def technical_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_technical:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def commercial_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_commercial:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def technical_or_commercial_or_superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_technical or request.user.is_commercial or request.user.is_superuser):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

