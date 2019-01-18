from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(request.get_full_path())


