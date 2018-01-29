# coding=utf-8
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.contrib.auth.middleware import get_user
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from functools import wraps
import jwt
import json


def get_jwt_token(request):
    try:
        token = request.stream.META.get('HTTP_AUTHORIZATION', None)
    except AttributeError:
        token = request.request.stream.META.get('HTTP_AUTHORIZATION', None)
    return token

def validate_jwt(view_func):
    @wraps(view_func)
    def new_view_func(request, *args, **kwargs):
        token = get_jwt_token(request)
        if token is not None:
            try:
                user_jwt = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=['HS256']
                )
                return view_func(request, *args, **kwargs)
            except jwt.ExpiredSignature or jwt.DecodeError or jwt.InvalidTokenError:  # NOQA
                data = {
                    'status': status.HTTP_403_FORBIDDEN,
                    'detail': 'Token invalido'
                }
            except Exception as e:
                data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'detail': e.args[0]
                }
            return HttpResponse(
                json.dumps(data),
                content_type='application/json',
                status=data['status']
            )
        else:
            return HttpResponse(
                {
                    'Error': "Internal server error"
                },
                status="500"
            )
    return new_view_func
