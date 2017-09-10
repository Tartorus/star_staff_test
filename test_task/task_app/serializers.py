from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post


class UserSerializer(serializers.ModelSerializer):

    registered_at = serializers.SerializerMethodField()
    posts_number = serializers.SerializerMethodField()
    posts_per_day = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'registered_at', 'posts_number', 'posts_per_day')

    def get_registered_at(self, obj):
        return obj.date_joined

    def get_posts_number(self, obj):
        return len(obj.posts.filter(user=obj).all())

    def get_posts_per_day(self, obj):
        post_count = self.get_posts_number(obj)
        d = timezone.now() - obj.date_joined
        if d.days > 0:
            result = round(post_count/d.days)
        else:
            result = post_count
        return result


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user', required=False)
    post_id = serializers.IntegerField(source='id', required=False, read_only=True)
    post_title = serializers.CharField(source='title')
    post_body = serializers.CharField(source='body')
    post_published_time = serializers.DateTimeField(source='published_time')

    class Meta:
        model = Post
        fields = ('username', 'post_id', 'post_title', 'post_body', 'post_published_time')

