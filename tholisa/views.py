from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
# https://docs.djangoproject.com/en/2.1/topics/auth/default/#the-login-required-decorator
# https://docs.djangoproject.com/en/2.1/topics/auth/default/#the-loginrequired-mixin
#
# for users on a per frontend base:
# https://docs.djangoproject.com/en/2.1/topics/auth/default/#limiting-access-to-logged-in-users-that-pass-a-test
# https://docs.djangoproject.com/en/2.1/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin
#
from .models import Pensis


def pensis_list(request):
    max_objects = 20
    thoughts = Pensis.objects.all()[:max_objects]
    data = {"results": list(thoughts.values("title", "headline", "content", "slug", "user__username", "pub_date"))}
    return JsonResponse(data)


def pensis_detail(request, pk):
    thought = get_object_or_404(Pensis, pk=pk)
    data = {"results": {
        "title": thought.title,
        "headline": thought.headline,
        "content": thought.content,
        "slug": thought.slug,
        "created_by": thought.user.username,
        "pub_date": thought.pub_date,
    }}
    return JsonResponse(data)
