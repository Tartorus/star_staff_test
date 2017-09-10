from lxml import etree
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from django.db.models import Count
from .serializers import UserSerializer, PostSerializer
from .models import Post


class UserList(generics.ListAPIView):
    """Api для работы с коллекцией пользователей.
    Доступные методы:
     GET
        Параметры: username - фильтрация пользователей по username
         posts_number - фильтрация по кол-ву постов. Выводятся пользователя с кол-вом постов равное или больше,
         чем posts_number """

    permission_classes = (IsAuthenticated, )

    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username', None)
        posts_number = self.request.query_params.get('posts_number', None)

        if username is not None:
            queryset = queryset.filter(username=username)
        if posts_number:
            queryset = queryset.annotate(post_count=Count('posts')).filter(post_count__gte=posts_number)
        return queryset


class SelfPostList(generics.CreateAPIView):
    """Api получения списка постов пользователя и создания нового поста
        Доступные методы: GET, POST."""

    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, format=None):
        posts = Post.objects.filter(user=request.user).all()
        posts = PostSerializer(posts, many=True)
        return Response(posts.data)


class SelfPostDetail(views.APIView):
    """Api обновления или удаления конкретного поста пользователя.
    Доступные методы: PUT, DELETE.
    """
    def get_object(self, post_id, user):
        try:
            return Post.objects.get(id=post_id, user=user)
        except Post.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def put(self, request, post_id, format=None):
        post = self.get_object(post_id, request.user)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, format=None):
        Post.objects.filter(id=post_id, user=request.user).delete()
        return Response()


class ImportXmlPosts(views.APIView):
    """Api импортирования постов в xml формате"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        new_posts = list()

        for xml_file in request.FILES.values():
            tree = etree.XML(xml_file.read())
            posts = tree.xpath('/posts/post')
            for post in posts:
                data = {child.tag: child.text for child in post.getchildren()}
                serializer = PostSerializer(data=data)
                if serializer.is_valid():
                    new_posts.append(serializer)
                    # result['new_posts'].append(serializer.save(user=request.user).id)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                #     result['errors'].append(serializer.errors)
        result = [serializer.save(user=request.user).id for serializer in new_posts]
        return Response(result)
