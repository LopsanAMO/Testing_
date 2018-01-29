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
from .serializers import ClientSerializer, AddressSerializer
from users.decorators import validate_jwt
from users.models import Client, Address
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
    @validate_jwt
    def post(self, request):
        data = request.data
        username = data.get('username')
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
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
                username,
                first_name,
                last_name,
                email,
                None,
                password
            )
            user_cls.save()
            return req_inf.status_200()
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
                if 'username' in data:
                    if self.validate_data(data.get('username'), user.username):
                        user.username = data.get('username')
                if 'email' in data:
                    if self.validate_data(data.get('email'), user_cls.user.email):
                        user.email = data.get('email')
                if 'password' in data:
                    user.set_password(data.get('password'))
                if 'phone' in data:
                    user_cls.phone = data.get('phone')
                if 'first_name' in data:
                    user.first_name = data.get('first_name')
                if 'last_name' in data:
                    user.last_name = data.get('last_name')
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


class AddresAPIView(APIView):
    @csrf_exempt
    def get(self, request):
        user = get_jwt_user(request)
        req_inf = RequestInfo()
        try:
            if user is not None:
                try:
                    serializer = AddressSerializer(
                        client.addresses.all(),
                        many=True
                    )
                    return Response(serializer.data)
                except ObjectDoesNotExist as e:
                    return req_inf.status_404(e.args[0])
                except Exception as e:
                    return req_inf.status_400(e.args[0])
            else:
                return req_inf.status_401('token invalido')
        except ObjectDoesNotExist as e:
            return req_inf.status_404(e.args[0])
        except Exception as e:
            return req_inf.status_400(e.args[0])

    @csrf_exempt
    @validate_jwt
    def post(self, request):
        user = get_jwt_user(request)
        data = request.data
        req_inf = RequestInfo()
        try:
            if user is not None:
                client = Client.objects.get(user=user)
                address = Address.create(
                    data.get('country'),
                    data.get('region'),
                    data.get('town'),
                    data.get('neighborhood'),
                    data.get('zip_code'),
                    data.get('street'),
                    data.get('street_number'),
                    data.get('suite_number')
                )
                client.addresses.add(address)
                client.save()
                return req_inf.status_200('address created')
            else:
                return req_inf.status_401('token invalido')
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
                client = Client.objects.get(user=user)
                address = Address.objects.get(id=data.get('address_id'))
                if 'country' in data:
                    address.country = data.get('country')
                if 'region' in data:
                    address.region = data.get('region')
                if 'town' in data:
                    address.town = data.get('town')
                if 'neighborhood' in data:
                    address.neighborhood = data.get('neighborhood')
                if 'zip_code' in data:
                    address.zip_code = data.get('zip_code')
                if 'street' in data:
                    address.street = data.get('street')
                if 'street_number' in data:
                    address.street_number = data.get('street_number')
                if 'suite_number' in data:
                    address.suite_number = data.get('suite_number')
                address.save()
                return req_inf.status_200('address updated')
            else:
                return req_inf.status_401('token invalido')
        except ObjectDoesNotExist as e:
            return req_inf.status_404(e.args[0])
        except Exception as e:
            return req_inf.status_400(e.args[0])


    @csrf_exempt
    @validate_jwt
    def delete(self, request):
        user = get_jwt_user(request)
        data = request.data
        req_inf = RequestInfo()
        try:
            if user is not None:
                client = Client.objects.get(user=user)
                address = Address.objects.get(id=data.get('address_id'))
                address.delete()
                return req_inf.status_200('address deleted')
            else:
                return req_inf.status_401('token invalido')
        except ObjectDoesNotExist as e:
            return req_inf.status_404(e.args[0])
        except Exception as e:
            return req_inf.status_400(e.args[0])
