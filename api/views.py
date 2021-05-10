from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, Group, Follow, User
from .permissions import IsOwnerOrReadOnly
from .serializers import CommentSerializer, PostSerializer, GroupSerializer, FollowSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group',]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        comments = post.comments.all()
        return comments


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'following']

    def perform_create(self, serializer):
        following = get_object_or_404(User, username=self.request.data.get('following'))
        follow = following.following.filter(following=following.id, user=self.request.user.id).exists()
        if not follow and self.request.user != following:
            serializer.save(user=self.request.user, following=following)

