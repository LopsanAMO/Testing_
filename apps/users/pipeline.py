#-*- encoding: utf-8 -*-
import sys
from .models import Client


def save_user(backend, user, response, is_new, details, *args, **kwargs):
    if is_new:
        model_user = user
        client = Client.objects.create(user=model_user)
        client.save()
