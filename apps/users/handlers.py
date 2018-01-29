from calendar import timegm
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_jwt.compat import get_username, get_username_field
from rest_framework_jwt.settings import api_settings
from users.api.v1.serializers import ClientSerializer


def jwt_payload_handler(user, request):
    username_field = get_username_field()
    username = get_username(user)
    payload = {
        'alpha': False,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'user_id': user.id,
        'user': ClientSerializer(user.client, context={'request': request}).data,
    }
    payload[username_field] = username
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(datetime.utcnow().utctimetuple())
    return payload


def generate_jwt(user, request):
    _jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    _jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = _jwt_payload_handler(user, request)
    return _jwt_encode_handler(payload)


def set_cookie_jwt(user, response):
    jwt = generate_jwt(user)
    response.set_cookie('token', jwt)
    return response
