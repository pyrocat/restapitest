from django.urls import include, path
from rest_framework import routers
from .users.views import UserViewSet, GroupViewSet
from .views import ProjectList, SnippetList, SnippetDetail, SnippetHighlight
from .authentication.views import RedmineTokenLoginView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('token-auth/', RedmineTokenLoginView.as_view(), name='api-token-auth'),
    path('projects/', ProjectList.as_view(), name='project-list'),
    path('users/', include(router.urls)),

    # Not really relevant at the moment
    path('snippets/', SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', SnippetDetail.as_view()),
    path('snippets/<int:pk>/highlighted', SnippetHighlight.as_view(), name='snippet-highlight'),
]