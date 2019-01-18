import re
import datetime
import json
import pytz
from rest_framework import exceptions, HTTP_HEADER_ENCODING

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.utils.six import text_type

from .models import Token


TOKEN_EXPIRE_TIME = datetime.timedelta(minutes=30)


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, text_type):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        absolute_path = request.get_full_path()
        exempted_urls = ['/api/v1/login']
        regex = re.match('/admin/', str(absolute_path))
        keyword = "Token"
        if absolute_path not in exempted_urls and not regex:
            auth = get_authorization_header(request).split()
            if not auth or auth[0].lower() != keyword.lower().encode():
                msg = {'error': 'No authentication header provided'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json', status=500)
                # return JsonResponse({'error': msg}, 500)

            if len(auth) == 1:
                msg = {'error': 'Invalid token header. No credentials provided.'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json', status=500)
            elif len(auth) > 2:
                msg = {'error': 'Invalid token header. Token string should not contain spaces.'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json', status=500)

            try:
                key = auth[1].decode()
            except UnicodeError:
                msg = {'error': 'Invalid token header. Token string should not contain invalid characters.'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json', status=500)

            model = Token

            try:
                token = model.objects.select_related('user').get(key=key)
            except model.DoesNotExist:
                msg = {'error': 'Invalid token'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json', status=500)

            utc_now = datetime.datetime.utcnow()
            utc_now = utc_now.replace(tzinfo=pytz.utc)

            if token.created < utc_now - TOKEN_EXPIRE_TIME:
                msg = {'error': 'Token has expired'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json', status=500)
            response = self.get_response(request)
            return response

