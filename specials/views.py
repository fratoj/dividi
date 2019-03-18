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
from django.views import generic
from django.views.generic.base import TemplateView
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from accounts.models import Author
from specials.forms import ExampleForm
from specials.serializers import ThoughtSerializer, FibSerializer
from .models import Thought, Fib
from rest_framework.response import Response
from rest_framework.views import APIView


def thought_list(request):
    max_objects = 20
    thoughts = Thought.objects.all()[:max_objects]
    data = {"results": list(thoughts.values("title", "headline", "content", "slug", "user__username", "pub_date"))}
    return JsonResponse(data)


def thought_detail(request, pk):
    thought = get_object_or_404(Thought, pk=pk)
    data = {"results": {
        "title": thought.title,
        "headline": thought.headline,
        "content": thought.content,
        "slug": thought.slug,
        "created_by": thought.user.username,
        "pub_date": thought.pub_date,
    }}
    return JsonResponse(data)


class HomeView(TemplateView):
    pass


class ThoughtView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk=None):
        if pk:
            thought = Thought.objects.get(pk=pk)
            serializer = ThoughtSerializer(thought, many=False)
        else:
            thought = Thought.objects.all()
            serializer = ThoughtSerializer(thought, many=True)
        return Response(serializer.data)

    def post(self, request):
        thought = request.data.get('thought')

        serializer = ThoughtSerializer(data=thought)
        if serializer.is_valid(raise_exception=True):
            saved_thought = serializer.save()
        return Response({
            'success': 'Your thought [{}] has been recorded and is ready for sharing'.format(saved_thought.title)
        })

    def put(self, request, pk):
        thought = get_object_or_404(Thought.objects.all(), pk=pk)
        data = request.data.get('thought')
        serializer = ThoughtSerializer(instance=thought, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_thought = serializer.save()

        return Response({
            'success': 'Thought [{}] updated successfully'.format(saved_thought.title)
        })

    def delete(self, request, pk):
        thought = get_object_or_404(Thought.objects.all(), pk=pk)
        thought.delete()
        return Response({
            'success': 'Thought [{}] deleted successfully'.format(thought.title)
        })


class FibView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Fib.objects.all()
    serializer_class = FibSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        user = get_object_or_404(Author, id=self.request.data.get('user'))
        return serializer.save(user=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SingleFibView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Fib.objects.all()
    serializer_class = FibSerializer


class FibIndexView(generic.ListView):
    form_class=ExampleForm
    model = Fib
    template_name = 'specials/fib_index_list.html'
