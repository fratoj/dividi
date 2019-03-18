from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Thought(models.Model):
    pub_date = models.DateField()
    create_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=80)
    headline = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )

    def __str__(self):
        return self.headline


class Fib(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=80)
    content = models.TextField()
    slug = models.SlugField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )

    def __str__(self):
        return self.title
