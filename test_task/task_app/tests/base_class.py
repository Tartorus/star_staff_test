import json
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate


class BaseClass(TestCase):
    """Базовый класс для тестирования"""

    fixtures = ['fixtures.json']

    url = None
    username = 'Ann'
    view = None

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.get(username=self.username)
        if self.view is None:
            raise ValueError('View is None')
        self.view = self.view.as_view()

    def auth_test(self, not_auth_status_code=401):
        """Апи доступное только для аутентифицированных пользвателей"""
        response = RequestFactory(self).get(auth=False)
        assert response.status_code == not_auth_status_code
        response = RequestFactory(self).get()
        assert response.status_code == 200


class RequestFactory:

    def __init__(self, test_instance, params=None, data=None):
        self.data = data
        self.view = test_instance.view
        self.user = test_instance.user

        if test_instance.url is None:
            raise ValueError('url is None')
        if params is None:
            self.url = test_instance.url
        else:
            self.url = test_instance.url + '?' + params

    def get(self, auth=True):
        request = APIRequestFactory().get(self.url, data=self.data)
        if auth:
            force_authenticate(request, user=self.user)
        return self.view(request)

    def post(self, auth=True):
        request = APIRequestFactory().post(self.url, data=self.data)
        if auth:
            force_authenticate(request, user=self.user)
        return self.view(request)

    def put(self, auth=True, **kwargs):
        request = APIRequestFactory().put(self.url, data=self.data)
        if auth:
            force_authenticate(request, user=self.user)
        return self.view(request, **kwargs)

    def delete(self, auth=True, **kwargs):
        request = APIRequestFactory().delete(self.url)
        if auth:
            force_authenticate(request, user=self.user)
        return self.view(request, **kwargs)
