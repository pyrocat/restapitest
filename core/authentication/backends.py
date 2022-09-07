from django.contrib.auth.backends import BaseBackend
from redmine.models import HelpdeskUser, RedmineToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

REMOTE_USER_MODEL = HelpdeskUser

from loguru import logger
logger.add('backend.log')


class RedmineTokenAuthentication(BaseBackend):
    """
    Provides authentication against remote database.
    """

    def authenticate(self, request, **kwargs):

        try:
            username = kwargs.get('username')
            remote_key = kwargs.get('remote_key')
            hd_user = REMOTE_USER_MODEL.objects.get(login=username,  # too dependent on the remote model, rearrange later
                                                    redminetoken__value=remote_key)
            logger.info(f'Found remote user: <{hd_user}>')
        except HelpdeskUser.DoesNotExist:
            raise AuthenticationFailed

        self.user, _ = User.objects.get_or_create(username=hd_user.login)

        logger.info(f'Returning local user <{self.user}>')
        return self.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


