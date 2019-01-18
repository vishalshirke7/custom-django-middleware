import re
import datetime
import json
import pytz

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.utils.six import text_type

from rest_framework import exceptions, HTTP_HEADER_ENCODING
from .models import Token


TOKEN_EXPIRE_TIME = datetime.timedelta(minutes=30)


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, text_type):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


def authenticate_credentials(key):
    model = Token

    try:
        token = model.objects.select_related('user').get(key=key)
    except model.DoesNotExist:
        raise exceptions.AuthenticationFailed(_('Invalid token.'))

    utc_now = datetime.datetime.utcnow()
    utc_now = utc_now.replace(tzinfo=pytz.utc)

    if token.created < utc_now - TOKEN_EXPIRE_TIME:
        raise exceptions.AuthenticationFailed('Token has expired')

    return token.user, token


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        absolute_path = request.get_full_path()
        exempted_urls = ['/api/v1/login']
        regex = re.match('/admin/', absolute_path)
        keyword = "Token"
        if absolute_path not in exempted_urls and not regex:
            auth = get_authorization_header(request).split()
            if not auth or auth[0].lower() != keyword.lower().encode():
                msg = {'error': 'No authentication header provided'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json')
                # return JsonResponse({'error': msg}, 500)

            if len(auth) == 1:
                msg = {'error': 'Invalid token header. No credentials provided.'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json')
            elif len(auth) > 2:
                msg = {'error': 'Invalid token header. Token string should not contain spaces.'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json')

            try:
                key = auth[1].decode()
            except UnicodeError:
                msg = {'error': 'Invalid token header. Token string should not contain invalid characters.'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json')

            model = Token

            try:
                token = model.objects.select_related('user').get(key=key)
            except model.DoesNotExist:
                msg = {'error': 'Invalid token'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json')

            utc_now = datetime.datetime.utcnow()
            utc_now = utc_now.replace(tzinfo=pytz.utc)

            if token.created < utc_now - TOKEN_EXPIRE_TIME:
                msg = {'error': 'Token has expired'}
                data = json.dumps(msg)
                return HttpResponse(data, content_type='application/json')
            response = self.get_response(request)
            return response

