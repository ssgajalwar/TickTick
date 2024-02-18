# yourappname/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

class AdminAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            return None

        if user.check_password(password) and user.groups.filter(name='admin').exists():
            return user

class StudentAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            return None

        if user.check_password(password) and user.groups.filter(name='student').exists():
            return user

class TeacherAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=username)
        except user_model.DoesNotExist:
            return None

        if user.check_password(password) and user.groups.filter(name='teacher').exists():
            return user
