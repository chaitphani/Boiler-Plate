from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.admin.sites import AlreadyRegistered
from django.apps import apps

# UnRegister your models here.

admin.site.unregister(User)
admin.site.unregister(Group)

# Register your models here.
# admin.site.register(Regmodel)

app_models = apps.get_app_config('Auth_app').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass