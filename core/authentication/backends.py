from rest_framework.authentication import TokenAuthentication

from redmine.models import HelpdeskUser, RedmineToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

REMOTE_USER_MODEL = HelpdeskUser

from loguru import logger
logger.add('backend.log')


class RedmineTokenAuthentication(TokenAuthentication):
    keyword = 'Token'
    model = None

    def authenticate(self, request):
        remote_credentials = self._get_remote_credentials(request)

        logger.info(f'Got remote_credentials <{remote_credentials}>')

        try:
            username = remote_credentials.get('username')
            remote_key = remote_credentials.get('remote_key')
            hd_user = REMOTE_USER_MODEL.objects.get(login=username,  # too dependent on the remote model, rearrange later
                                                    redminetoken__value=remote_key)
            logger.info(f'Found hd_user: <{hd_user}>')
        except HelpdeskUser.DoesNotExist:
            raise AuthenticationFailed

        self.user, _ = User.objects.get_or_create(username=hd_user.login)

        self.user.save()
        token_model = self.get_model()
        token, _ = token_model.objects.get_or_create(user=self.user)

        logger.info(f'Returning user and token <{self.user}> <{token}>')
        return self.user, token


    def authenticate_header(self, request):
        return self.keyword

    def _get_remote_credentials(self, request):
        logger.info(f'request.POST <{request.POST}>')
        remote_auth_kwargs = {
            "username": request.POST["username"],
            "remote_key": request.POST["remote_key"],  # too dependent on the serializer field name
            #  TODO choose more general naming later
        }
        return remote_auth_kwargs
