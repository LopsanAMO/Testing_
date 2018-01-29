from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import login, UserAPI



urlpatterns = [
    path('login', csrf_exempt(login), name='login'),
    path('user', csrf_exempt(UserAPI.as_view()), name='user_list')
]
