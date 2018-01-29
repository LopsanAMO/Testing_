from django.urls import path, include
from users.api.v1 import urls as UserUrls

urlpatterns = [
    path('users/', include(UserUrls))
]
