from django.conf import settings


def modules(request):
    return {
        "GPIO_ENABLED": bool(settings.GPIO),
    }


def resolver(request):
    return {
        "app_name": request.resolver_match.app_name,
        "url_name": request.resolver_match.url_name,
        "namespace": request.resolver_match.namespace,
    }
