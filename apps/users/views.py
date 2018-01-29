from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from .models import Client, Address
from .forms import AddressForm


class UserView(View):
    def get(self, request):
        """User View GET
        Description:
            render view to create users
        """
        template_name = 'new_user.html'
        return render(request, template_name)

    def post(self, request):
        """User View Post
        Args:
            email (str): email del usuario
            username (str): nombre de usuario
            first_name (str): nombres
            last_name (str): apellidos
            phone (str): telefono
            password (str): contraseña
        """
        template_name = 'new_user.html'
        try:
            _user = User.objects.get(
                Q(
                    email=request.POST.get('email')
                ) | Q(
                    username=request.POST.get('username')
                ))
            messages.error(request, 'Email ya registrado, prueba con otro')
            return HttpResponseRedirect('.')
        except ObjectDoesNotExist:
            pass
        try:
            user = Client.create(
                request.POST.get('username'),
                request.POST.get('first_name', None),
                request.POST.get('last_name', None),
                request.POST.get('email'),
                request.POST.get('phone', None),
                request.POST.get('password')
            )
            return redirect('/')
        except Exception as e:
            messages.error(request, e.args[0])
            return HttpResponseRedirect('/')


class Home(View):
    def get(self, request):
        """Home View GET
        render view to home page
        """
        template_name = 'home.html'
        users = Client.objects.all()
        context = {
            'users': users
        }
        return render(request, template_name, context)

    def post(self, request):
        """Home View Post
        Args:
            action (int): accion requerida
            email (str): email del usuario
            username (str): nombre de usuario
            password (str): contraseña
        Returns:
            acction (1): django session
            action (2): new user and django session
        """
        action = request.POST.get('action')
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password')
        if action == '1':
            try:
                if '@' in email:
                    try:
                        u = User.objects.get(email=email)
                    except User.DoesNotExist:
                        pass
                    else:
                        username = u.username
                user = authenticate(username=username, password=password)
                login(
                    request,
                    user,
                    backend='django.contrib.auth.backends.ModelBackend'
                )
                return redirect('/')
            except Exception as e:
                messages.error(request, e.args[0])
                return HttpResponseRedirect('.')
        else:
            try:
                user = User.objects.get(Q(email=email) | Q(username=username))
                messages.error(request, 'Email ya registrado, prueba con otro')
                return HttpResponseRedirect('.')
            except ObjectDoesNotExist:
                pass
            try:
                user = Client.create(
                    username, None, None, email, None, password)
                login(
                    request,
                    user.user,
                    backend='django.contrib.auth.backends.ModelBackend'
                )
                return redirect('/')
            except Exception as e:
                messages.error(request, e.args[0])
                return HttpResponseRedirect('.')


@login_required
def user_edit(request, pk=None):
    """User Edit View
    Args:
        email (str): email del usuario
        username (str): nombre de usuario
        first_name (str): nombres
        last_name (str): apellidos
        phone (str): telefono
        password (str): contraseña
    """
    user = None
    try:
        user = Client.objects.get(id=pk)
    except Exception as e:
        messages.error(request, e.args[0])
        return HttpResponseRedirect('.')
    if request.method == 'GET':
        template_name = 'edit_user.html'
        context = {
            'user': user
        }
        return render(request, template_name, context)
    else:
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        phone = request.POST.get('phone', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        user = request.user
        _user = user.client
        try:
            if username not in ['', ' ', None]:
                user.username = username
            if email not in ['', ' ', None]:
                user.email = email
            if password not in ['', ' ', None]:
                user.set_password(password)
            if phone not in ['', ' ', None]:
                _user.phone = phone
            if first_name not in ['', ' ', None]:
                user.first_name = first_name
            if last_name not in ['', ' ', None]:
                user.last_name = last_name
            _user.save()
            user.save()
            return redirect('/')
        except Exception as e:
            messages.error(request, e.args[0])
            return HttpResponseRedirect('.')


@login_required
def user_delete(request, pk=None):
    """User Delete View
    Description:
        view to delete users
    """
    try:
        user = Client.objects.get(id=pk)
    except Exception as e:
        messages.error(request, e.args[0])
        return HttpResponseRedirect('.')
    if request.method == 'GET':
        _user = user.user
        _user.delete()
        return redirect('/')
    else:
        messages.error(request, e.args[0])
        return HttpResponseRedirect('.')


@login_required
def address_list(request, pk=None):
    template_name = 'list_address.html'
    try:
        addresses = Client.objects.get(id=pk).addresses.all()
        context = {
            'addresses': addresses
        }
    except Exception:
        context = {
            'addresses': []
        }
    try:
        context['users'] = Client.objects.get(id=pk)
    except Exception as e:
        messages.error(request, e.args[0])
        return HttpResponseRedirect('/')
    return render(request, template_name, context)


@login_required
def address_new(request, pk=None):
    if request.method == 'GET':
        template_name = 'new_address.html'
        form = AddressForm()
        context = {
            'form': form
        }
        return render(request, template_name, context)
    else:
        try:
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.save()
                client = Client.objects.get(id=pk)
                client.addresses.add(address)
                return redirect('/user/address/list/{}/'.format(pk))
        except Exception as e:
            messages.error(request, e.args[0])
            return HttpResponseRedirect('.')



@login_required
def address_edit(request, pk=None):
    template_name = 'edit_address.html'
    if request.method == 'GET':
        try:
            address = Address.objects.get(id=pk)
            context = {
                'address': address
            }
            return render(request, template_name, context)
        except Exception as e:
            messages.error(request, e.args[0])
            return redirect('/')
    else:
        try:
            address = Address.objects.get(id=pk)
            if request.POST['region'] is not None:
                address.region = request.POST.get('region')
            if request.POST['town'] is not None:
                address.town = request.POST.get('town')
            if request.POST['neighborhood'] is not None:
                address.neighborhood = request.POST.get('neighborhood')
            if request.POST['zip_code'] is not None:
                address.zip_code = request.POST.get('zip_code')
            if request.POST['street'] is not None:
                address.street = request.POST.get('street')
            if request.POST['street_number'] is not None:
                address.street_number = request.POST.get('street_number')
            if request.POST['suite_number'] is not None:
                address.suite_number = request.POST.get('suite_number')
            if request.POST['country'] is not None:
                address.country = request.POST.get('country')
            address.save()
            return redirect('/')
        except Exception as e:
            messages.error(request, e.args[0])
            return HttpResponseRedirect('/')


@login_required
def address_delete(request, pk=None):
    address = None
    try:
        address = Address.objects.get(id=pk)
        address.delete()
        return redirect('/')
    except Exception as e:
        messages.error(request, e.args[0])
        return redirect('/')
