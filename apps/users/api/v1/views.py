from django.shortcuts import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.handlers import generate_jwt
from .serializers import ClientSerializer
from users.decorators import validate_jwt
from users.models import Client
from utils.helpers import RequestInfo, get_jwt_user


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny, ))
def login(request):
    """Login API View
    Args:
        username (str): user email
        password (str): user password
    """
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    req_info = RequestInfo()
    if '@' in username:
        try:
            u = User.objects.get(email=username)
        except User.DoesNotExist:
            pass
        else:
            username = u.username
    try:
        user = authenticate(username=username, password=password)
    except ObjectDoesNotExist:
        user = None
    if user is not None:
        return Response({'token': generate_jwt(user, request)})
    else:
        return req_info.status_400('email o password incorrectos')


class UserAPI(APIView):
    @csrf_exempt
    def get(self, request):
        user = get_jwt_user(request)
        req_inf = RequestInfo()
        if user is not None:
            try:
                serializer = ClientSerializer(user.client)
                return Response(serializer.data)
            except ObjectDoesNotExist as e:
                return req_inf.status_404(e.args[0])
            except Exception as e:
                return req_inf.status_400(e.args[0])
        else:
            return req_inf.status_401('token invalido')

    @csrf_exempt
    @permission_classes((AllowAny, ))
    def post(self, request):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        req_inf = RequestInfo()
        user = None
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist as e:
            pass
        if user is not None:
            return req_inf.status_400('email already exists')
        try:
            user_cls = Client.create(
                username=username,
                email=email,
                password=password
            )
            user_cls.save()
            return Response({
                'token': generate_jwt(user_cls.user, request)},
                status=status.HTTP_200_OK
            )
        except ObjectDoesNotExist as e:
            return req_inf.status_404(e.args[0])
        except Exception as e:
            return req_inf.status_400(e.args[0])

    @csrf_exempt
    @validate_jwt
    def patch(self, request):
        user = get_jwt_user(request)
        data = request.data
        req_inf = RequestInfo()
        try:
            if user is not None:
                user_cls = Client.objects.get(user=user)
                if self.validate_data(data.get('name'), user_cls.name):
                    user_cls.name = data.get('name')
                if self.validate_data(data.get('email'), user_cls.user.email):
                    user.email = data.get('email')
                if 'password' in data:
                    user.set_password(data.get('password'))
                if 'phone' in data:
                    user.phone = data.get('phone')
                user.save()
                user_cls.save()
                data_err = {
                    'status': status.HTTP_200_OK,
                    'token': generate_jwt(user, request),
                    'detail': 'user updated'
                }
                return req_inf.return_status(data_err)
            else:
                return req_inf.status_401('token invalido')
        except ObjectDoesNotExist as e:
            return req_inf.status_404(e.args[0])
        except Exception as e:
            return req_inf.status_400(e.args[0])

    def validate_data(self, data, field):
        empty_list = ['', ' ', None]
        if data not in empty_list and data != field:
            return True
        else:
            return False
