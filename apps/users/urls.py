from django.urls import path
from .views import (
    UserView, user_edit, user_delete, address_new, address_edit,
    address_delete, address_list
)

app_name = 'users'
urlpatterns = [
    path('new/', UserView.as_view()),
    path('edit/<int:pk>/', user_edit, name='edit'),
    path('delete/<int:pk>/', user_delete, name='delete'),
    path('address/new/<int:pk>/', address_new, name='address_new'),
    path('address/edit/<int:pk>/', address_edit, name='address_edit'),
    path('address/delete/<int:pk>/', address_delete, name='address_delete'),
    path('address/list/<int:pk>/', address_list, name='address_list')
]
