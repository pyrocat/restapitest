from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from loguru import logger


class RedmineTokenLoginSerializer(serializers.Serializer):
    """
    Allows to login with redmine_key instead of a password
    """
    username = serializers.CharField(required=True)
    remote_key = serializers.CharField(required=True, write_only=True)

    token = serializers.ReadOnlyField(required=False)
    def validate(self, attrs):
        logger.info(f'Now validating attrs: <{attrs}>')

        authenticate_kwargs = {
            "username": attrs.get("username"),
            "remote_key": attrs.get("remote_key"),
        }

        logger.info(f'Now expecting to authenticate user with the attrs: <{authenticate_kwargs}>')

        user: User = authenticate(**authenticate_kwargs)

        if not user:
            logger.exception('User not found!')
        if not user.is_active:
            raise PermissionDenied(f'user {user} is not active')

        token, _ = Token.objects.get_or_create(user=user)

        logger.info(f'Validated user <{user}> with token key <{token.key}>')

        attrs['token'] = token.key

        return attrs
