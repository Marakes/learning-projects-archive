from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from api.views import CommentViewSet, GroupViewSet, PostViewSet


v1_router = DefaultRouter()
v1_router.register('posts', PostViewSet, basename='posts')
v1_router.register('groups', GroupViewSet, basename='groups')
v1_posts_router = NestedDefaultRouter(v1_router, r'posts', lookup='post')
v1_posts_router.register('comments', CommentViewSet, basename='post-comments')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(v1_posts_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
