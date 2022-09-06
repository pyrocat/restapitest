from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from redmine.models import HelpdeskUser, RedmineToken
from rest_framework.exceptions import AuthenticationFailed


class RedmineTokenLoginSerializer(serializers.Serializer):
    """
    Allows to login with redmine_key instead of password
    """
    username = serializers.CharField(required=True)
    redmine_key = serializers.CharField(required=True)

    def validate(self, attrs):
        try:
            username = attrs.get('username')
            redmine_key = attrs.get('redmine_key')
            hd_user = HelpdeskUser.objects.get(login=username, redminetoken__value=redmine_key)
        except HelpdeskUser.DoesNotExist:
            raise AuthenticationFailed

        user, _ = User.objects.get_or_create(username=hd_user.login)

        user.save()
        attrs['user'] = user

        return attrs
