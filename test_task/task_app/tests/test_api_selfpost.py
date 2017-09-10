import os
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from task_app.views import SelfPostList, SelfPostDetail, ImportXmlPosts
from task_app.serializers import PostSerializer
from task_app.models import Post
from .base_class import BaseClass, RequestFactory


class TestApiSelfPotsList(BaseClass):
    """Тестирование SelfPostList"""

    fixtures = ['fixtures.json']
    username = 'Ann'
    url = '/myposts/'
    view = SelfPostList

    def test_auth(self):
        self.auth_test()

    def test_get(self):
        """Получение списка посто пользователя"""
        posts = Post.objects.filter(user=self.user).all()
        posts = PostSerializer(posts, many=True)
        response = RequestFactory(self).get()
        self.assertEqual(posts.data, response.data)

    def test_post(self):
        """Добавление нового поста"""
        count = Post.objects.filter(user=self.user).count()
        response = RequestFactory(self, data=
            dict(
                post_title='Title',
                post_body='body',
                post_published_time='2017-08-20 10:30:00'
            )
        ).post()

        self.assertEqual(response.status_code, 201)
        new_count = Post.objects.filter(user=self.user).count()
        self.assertEqual(count + 1, new_count)


class TestApiSelfPotsDetail(BaseClass):
    """Тестирование SelfPostList"""

    fixtures = ['fixtures.json']
    username = 'Ann'
    url = '/myposts/'
    view = SelfPostDetail

    def test_put(self):
        """Обновление поста"""
        post = Post.objects.filter(user=self.user).first()
        response = RequestFactory(self, data=
            dict(
                post_title='NewTitle',
                post_body='NewBody',
                post_published_time='2017-08-20 10:30:00'
            )
        ).put(post_id=post.id)

        updated_post = Post.objects.get(id=post.id)
        updated_post = PostSerializer(updated_post)
        self.assertEqual(response.data, updated_post.data)

    def test_delete(self):
        """Удаление поста"""
        count = Post.objects.filter(user=self.user).count()
        post = Post.objects.filter(user=self.user).first()
        response = RequestFactory(self).delete(post_id=post.id)
        self.assertEqual(response.status_code, 200)
        new_count = Post.objects.filter(user=self.user).count()
        self.assertEqual(count - 1, new_count)


class TestApiImportPosts(BaseClass):
    """Тестирование импортирования постов"""

    fixtures = ['fixtures.json']
    username = 'Ann'
    url = '/myposts/import_xml/'
    view = ImportXmlPosts

    def prepare(self, filename):
        file_dir = os.getcwd() + '/task_app/tests/{}'.format(filename)
        file = File(open(file_dir, 'rb'))
        return SimpleUploadedFile(filename, file.read(), content_type='multipart/form-data')

    def test_import_success(self):
        """Ипортирование валидного xml"""

        uploaded_file = self.prepare('post_valid.xml')
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = reverse('import_xml')
        count = Post.objects.filter(user=self.user).count()
        client.post(url, {'file': uploaded_file}, format='multipart')
        new_count = Post.objects.filter(user=self.user).count()
        self.assertEqual(new_count, count + 2)

    def test_import_failed(self):
        """Ипортирование не валидного xml"""

        uploaded_file = self.prepare('post_invalid.xml')
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = reverse('import_xml')
        count = Post.objects.filter(user=self.user).count()
        response = client.post(url, {'file': uploaded_file}, format='multipart')
        new_count = Post.objects.filter(user=self.user).count()
        self.assertEqual(new_count, count)
        self.assertEqual(response.status_code, 400)
