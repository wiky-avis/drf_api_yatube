from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet, GroupViewSet, FollowViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(
    r'posts/(?P<id>[0-9]+)/comments', CommentViewSet, basename='comments')
router.register(r'follow', FollowViewSet)
router.register(r'group', GroupViewSet)

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'),
]
