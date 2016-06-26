# -*- coding: utf-8 -*-
# Author: Nutart
# Author Uri: http://nutart.com

from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', related_query_name='post')
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)
    terms = models.ManyToManyField('Term', related_name='posts', related_query_name='post')


class PostType(models.Model):
    name = models.TextField()


class BaseMeta(models.Model):
    key = models.CharField(max_length=255)
    value = models.TextField()

    class Meta():
        abstract = True


class PostMeta(BaseMeta):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='metas', related_query_name='meta')


class Taxonomy(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)


class Term(models.Model):
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, related_name='terms', related_query_name='term')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', related_query_name='comment', null=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)


class AnoyComment(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    ip = models.CharField(max_length=100)


class Setting(BaseMeta):
    autoload = models.BooleanField(default=False)
