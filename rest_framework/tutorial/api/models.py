from django.db import models

from django.contrib.auth.models import User


class BlogModel(models.Model):
    title = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    author = User
    tag = models.ForeignKey('TagModel', blank=True, on_delete=models.CASCADE)
    body = models.TextField()

    class Meta:
        ordering = ['-create_time']


class TagModel(models.Model):
    name = models.CharField(max_length=20)
