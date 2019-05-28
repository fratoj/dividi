from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Author
from specials import tomd
from specials.forms import FibForm
from specials.serializers import ThoughtSerializer, FibSerializer
from .models import Thought, Fib


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
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = get_object_or_404(Author, id=self.request.data.get('user'))
        return serializer.save(user=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SingleFibView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Fib.objects.all()
    serializer_class = FibSerializer


class FibCreateView(LoginRequiredMixin, CreateView):
    form_class = FibForm
    model = Fib

    # template_name = 'specials/fib_index_list.html'

    def get_success_url(self):
        return reverse('specials:fib_list')

    def form_valid(self, form):
        fib = form.save(commit=False)
        fib.content = tomd.convert(fib.content)
        loggedin_user = Author.objects.get(id=self.request.user.id)
        fib.user = loggedin_user
        fib.save()
        return HttpResponseRedirect(self.get_success_url())


class FibIndexView(ListView):
    model = Fib
    fields = ('title', 'content', 'user',)
    ordering = ['-create_date']

    def get(self, request, *args, **kwargs):
        print('Bla bla bla ...')
        return super(FibIndexView, self).get(request, *args, **kwargs)


class FibDetailView(DetailView):
    model = Fib
