from rest_framework import serializers
from django.contrib.auth.models import User, Group

from core.serializers import SnippetSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = SnippetSerializer( many=True, read_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'snippets']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']