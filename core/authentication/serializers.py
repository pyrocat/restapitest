from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed

from loguru import logger

class RedmineTokenLoginSerializer(serializers.Serializer):
    """
    Allows to login with redmine_key instead of a password
    """
    username = serializers.CharField(required=True)
    remote_key = serializers.CharField(required=True)

    def validate(self, attrs):
        logger.info(f'Now validating attrs: <{attrs}>')

        authenticate_kwargs = {
            "username": attrs.get("username"),
            "remote_key": attrs.get("remote_key"),
        }

        # Here's the validation part
        logger.info(f'Now expecting to authenticate user with the attrs: <{authenticate_kwargs}>')
        user = authenticate(**authenticate_kwargs)
        if not user:
            logger.exception('User not found!')
        if not user.is_active:
            raise PermissionDenied(f'user {user} is not active')

        logger.info(f'Validated user <{user}>')
        attrs['user'] = user

        return attrs
