from task_app.views import UserList
from django.contrib.auth.models import User
from task_app.serializers import UserSerializer
from .base_class import BaseClass, RequestFactory


class TestApiUserList(BaseClass):
    """Тестирование UserList"""

    fixtures = ['fixtures.json']
    username = 'Ann'
    url = '/users'
    view = UserList

    def test_auth(self):
        self.auth_test()

    def test_userlist(self):
        """Запрос без параметров"""
        response = RequestFactory(self).get()
        assert len(response.data) == 4

    def test_userlist_param(self):
        """С query параметрами"""
        response = RequestFactory(self, params='username=Ann').get()
        users = User.objects.filter(username='Ann').all()
        users = UserSerializer(users, many=True)
        self.assertEqual(response.data, users.data)
        response = RequestFactory(self, params='posts_number=2').get()
        self.assertEqual(len(response.data), 3)

