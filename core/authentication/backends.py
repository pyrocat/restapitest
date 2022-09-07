from rest_framework.authentication import TokenAuthentication

from redmine.models import HelpdeskUser, RedmineToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

REMOTE_USER_MODEL = HelpdeskUser

from pprint import pprint

class RedmineTokenAuthentication(TokenAuthentication):
    keyword = 'Token'
    model = None

    def authenticate(self, request):

        remote_credentials = self._get_remote_credentials(request)
        print(f'remote_credentials {remote_credentials}')
        try:
            username = remote_credentials.get('username')
            remote_key = remote_credentials.get('remote_key')
            hd_user = REMOTE_USER_MODEL.objects.get(login=username,  # too dependent on the remote model, rearrange later
                                                    redminetoken__value=remote_key)
            print(f'hd_user {hd_user}')
        except HelpdeskUser.DoesNotExist:
            raise AuthenticationFailed

        self.user, _ = User.objects.get_or_create(username=hd_user.login)

        self.user.save()
        token_model = self.get_model()
        token, _ = token_model.objects.get_or_create(user=self.user)

        print(f' token.user, token {token.user, token}')
        return (token.user, token)


    def authenticate_header(self, request):
        return self.keyword

    def _get_remote_credentials(self, request):
        pprint(f'request key {request.POST}')
        remote_auth_kwargs = {
            "username": request.POST["username"],
            "remote_key": request.POST["remote_key"],  # too dependent on the serializer field name
            #  TODO choose more general naming later
        }
        return remote_auth_kwargs
