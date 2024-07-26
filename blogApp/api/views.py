from urllib import request
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from blogApp.models import (
    BlogPost,
    Category,
    Comment,
    Like,
    View
)
from .serializers import (
    CategorySerializer,
    BlogPostSerializer,
    CommentSerializer,
    LikeSerializer,
    PostUserSerializer,
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

class CommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        blog = get_object_or_404(BlogPost, slug=slug)
        user = self.request.user
        comments = Comment.objects.filter(post=blog, user=user)
        if comments.exists():
            raise ValidationError(
                "You can not add another comment, for this Post !")
        serializer.save(post=blog, user=user)   

class LikeView(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user_id')
        post = request.data.get('post')
        serializer = self.get_serializer(data=request.data)
        exists_like = Like.objects.filter(user_id=user, post=post)
        serializer.is_valid(raise_exception=True)
        if exists_like:
            exists_like.delete()
        else:
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    


class UserAllPosts(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    # permission_classes = [IsPostOwnerOrReadOnly]

    def get_queryset(self):
        author = self.request.user
        queryset = BlogPost.objects.filter(author=author)
        return queryset   

class PostUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = PostUserSerializer
    # permission_classes = [permissions.IsAuthenticated]     