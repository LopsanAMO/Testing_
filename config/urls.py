from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth
from api import urls as APIV1Urls
from users import urls as UserUrls
from users.views import Home, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(APIV1Urls)),
    path('user/', include('users.urls')),
    path('', Home.as_view()),
    path('', include('social_django.urls', namespace='social')),
    path('logout/', auth.logout, {'next_page': '/'}, name='logout'),
]
