from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views
from .views import UserViewSet, GroupViewSet, SnippetList, SnippetDetail, SnippetHighlight


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('snippets/', SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', SnippetDetail.as_view()),
    path('snippets/<int:pk>/highlighted', SnippetHighlight.as_view(), name='snippet-highlight'),
    path('token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]