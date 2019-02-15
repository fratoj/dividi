from django.utils.text import slugify
from rest_framework import serializers

from accounts.models import Ibutho
from .models import Pensis, Fib


class PensisSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=80)
    headline = serializers.CharField(required=True, allow_blank=False, max_length=200)
    content = serializers.CharField(required=True)
    slug = serializers.SlugField(required=False)
    user = serializers.CharField(required=True)
    pub_date = serializers.DateField(required=True)

    def create(self, validated_data):
        posted_user = Ibutho.objects.filter(id=validated_data['user']).first()
        validated_data['user'] = posted_user
        validated_data['slug'] = slugify(validated_data['title'])
        return Pensis.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.headline = validated_data.get('headline', instance.headline)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.content = validated_data.get('content', instance.content)
        posted_user = Ibutho.objects.filter(id=validated_data.get('user', instance.user.id)).first()
        instance.user = posted_user
        instance.save()
        return instance


class FibSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fib
        fields = ('id', 'title', 'content', 'slug', 'user')

# class FibSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=True, allow_blank=False, max_length=80)
#     content = serializers.CharField(required=True)
#     slug = serializers.SlugField(required=False)
#     user = serializers.CharField(required=True)
#
#     def create(self, validated_data):
#         posted_user = Ibutho.objects.filter(id=validated_data['user']).first()
#         validated_data['user'] = posted_user
#         validated_data['slug'] = slugify(validated_data['title'])
#         return Fib.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.content = validated_data.get('content', instance.content)
#         posted_user = Ibutho.objects.filter(id=validated_data.get('user', instance.user.id)).first()
#         instance.user = posted_user
#         instance.save()
#         return instance
