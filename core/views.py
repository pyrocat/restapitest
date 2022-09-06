from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication

from core.models import Snippet
from core.serializers import SnippetSerializer

from redmine.serializers import ProjectSerializer
from rest_framework.response import Response

from rest_framework import generics, renderers
from rest_framework.reverse import reverse

from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView

from redmine.models import Project

class ApiRoot(APIView):
    """
    Root endpoint for the API
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, format=None):
        return Response(
            {
                'projects': reverse('project-list', request=request, format=format),
                'users': reverse('user-list', request=request, format=format)
            }
        )

class ProjectList(generics.ListAPIView):
    """
    Lists Redmine Projects related to the user
    """
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated,]
    def get_queryset(self):
        user = self.request.user
        print(f'Username to search against {user.username}')
        projects = Project.objects.filter(member__user__login=user.username)
        return projects



# Code below is not relevant at the moment

class SnippetList(generics.ListCreateAPIView):
    """
    List all snippets, or create a new snippet.
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View details for a Snippet
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetHighlight(generics.GenericAPIView):
    """
    Renders highlighted code field as HTML
    """
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
