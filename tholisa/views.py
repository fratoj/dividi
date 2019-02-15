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
from rest_framework.permissions import IsAuthenticated

from tholisa.serializers import PensisSerializer
from .models import Pensis
from rest_framework.response import Response
from rest_framework.views import APIView


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


class PensisView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        pensis = Pensis.objects.all()
        serializer = PensisSerializer(pensis, many=True)
        return Response(serializer.data)

    def post(self, request):
        pensis = request.data.get('pensis')

        serializer = PensisSerializer(data=pensis)
        if serializer.is_valid(raise_exception=True):
            saved_pensis = serializer.save()
        return Response({
            'success': 'Your thought [{}] has been recorded and is ready for sharing'.format(saved_pensis.title)
        })

    def put(self, request, pk):
        thought = get_object_or_404(Pensis.objects.all(), pk=pk)
        data = request.data.get('pensis')
        serializer = PensisSerializer(instance=thought, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_thought = serializer.save()

        return Response({
            'success': 'Thought [{}] updated successfully'.format(saved_thought.title)
        })

    def delete(self, request, pk):
        thought = get_object_or_404(Pensis.objects.all(), pk=pk)
        thought.delete()
        return Response({
            'success': 'Thought [{}] deleted successfully'.format(thought.title)
        })
