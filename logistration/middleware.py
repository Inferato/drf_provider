from django.http import HttpResponseForbidden


class SimpleAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.GET.get('is_pass_asuth_check') == 'true':
            response = self.get_response(request)
        else:
            response = HttpResponseForbidden()

        return response