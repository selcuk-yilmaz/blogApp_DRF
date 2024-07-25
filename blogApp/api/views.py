from urllib import request
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from blogApp.models import (
    BlogPost,
    Category,
    # Comment,
    # Like,
    View
)
from .serializers import (
    CategorySerializer,
    BlogPostSerializer,
    # LikeSerializer,
    # CommentSerializer,
    # PostUserSerializer,
    # ViewSerializer
)
from rest_framework import permissions
# from .pagination import CustomLimitOffsetPagination
# from .permissions import IsPostOwnerOrReadOnly, IsAdminUserOrReadOnly
from django.contrib.auth import get_user_model
# User = settings.AUTH_USER_MODEL
User = get_user_model()


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminUserOrReadOnly]

class BlogPostView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.filter(status="p")
    serializer_class = BlogPostSerializer
    # pagination_class = CustomLimitOffsetPagination
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) 

class UserAllPosts(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    # permission_classes = [IsPostOwnerOrReadOnly]

    def get_queryset(self):
        author = self.request.user
        queryset = BlogPost.objects.filter(author=author)
        return queryset


class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "slug"
    # permission_classes = [IsPostOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # View.objects.get_or_create(user=request.user, post=instance)
        View.objects.create(user=request.user, post=instance)
        return Response(serializer.data)         