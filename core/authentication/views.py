from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from .serializers import RedmineTokenLoginSerializer


class RedmineTokenLoginView(ObtainAuthToken):
    """
    This view uses custom RedmineTokenLoginSerializer to authenticate local user against remote database.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RedmineTokenLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)

