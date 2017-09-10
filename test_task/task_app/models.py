from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):

    user = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    published_time = models.DateTimeField(default=timezone.now, null=False)
