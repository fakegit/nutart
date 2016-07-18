# -*- coding: utf-8 -*-
# Author: Nutart
# Author Uri: http://nutart.com

import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.text import slugify


class Entry(models.Model):
    # POST_STATUS_CHOICES = (
    #     ('draft', 'Draft'),
    #     ('published', 'Published')
    # )
    # COMMENT_STATUS_CHOICES = (
    #     ('open', 'Open'),
    #     ('close', 'Close')
    # )
    title = models.TextField('title')
    slug = models.SlugField(max_length=255)
    content = models.TextField(blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts', related_query_name='post')
    ctime = models.DateTimeField('created time', auto_now_add=True)
    ptime = models.DateTimeField('published time', default=timezone.now)
    mtime = models.DateTimeField('modified time', auto_now=True)
    terms = models.ManyToManyField('Term', related_name='posts', related_query_name='post')
    # post_status = models.CharField(max_length=20, choices=POST_STATUS_CHOICES, default='')
    # comment_status = models.CharField(max_length=20, choices=COMMENT_STATUS_CHOICES)
    comment_count = models.BigIntegerField(default=0)
    # template = models.CharField(max_length=255)

    class Meta:
        ordering = ['-ptime']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        posttype = self.terms.get(taxonomy__name='posttype').slug
        return reverse('nutcms:movie', args=[str(posttype), str(self.slug)])


class EntryMeta(models.Model):
    post = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='metas', related_query_name='meta')
    key = models.CharField(max_length=255)
    value = models.TextField(blank=True)


class Taxonomy(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name_plural = 'taxonomies'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.unique_slug()
        super(Taxonomy, self).save(*args, **kwargs)

    def unique_slug(self):
        self.slug = slugify(self.name)
        while Taxonomy.objects.filter(slug=self.slug).exclude(name=self.name).exists():
            self.slug = '-'.join((self.slug, str(uuid.uuid4())[:8]))

    def get_absolute_url(self):
        return reverse('nutcms:taxonomy', args=[str(self.slug)])


class Term(models.Model):
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, related_name='terms', related_query_name='term')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200)
    # parent = models.BigIntegerField(default=0)
    count = models.BigIntegerField(default=0)
    # template = models.CharField(max_length=255)
    registered_taxonomies = models.ManyToManyField(Taxonomy, related_name='registered_terms', related_query_name='registered_term')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('nutcms:term', args=[str(self.taxonomy.slug), str(self.slug)])


class TermMeta(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='metas', related_query_name='meta')
    key = models.CharField(max_length=255)
    value = models.TextField(blank=True)


class Comment(models.Model):
    post = models.ForeignKey('Entry', on_delete=models.CASCADE, related_name='comments', related_query_name='comment')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments', related_query_name='comment', null=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.id


class AnoyComment(models.Model):
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.id


class Option(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField(blank=True)
    autoload = models.BooleanField(default=False)

class MovieResource(models.Model):
    post = models.OneToOneField(Entry, on_delete=models.CASCADE)
    movie = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name='resources', related_query_name='resource')