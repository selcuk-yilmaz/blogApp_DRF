from django.urls import path
from blogApp.api.views import (
    CategoryView,
    BlogPostView,
    BlogPostDetailView,
    # LikeView,
    # CommentView,
    # PostUserView,
    # UserAllPosts
)


urlpatterns = [
    path("category/", CategoryView.as_view()),
    path("posts/", BlogPostView.as_view()),
    path("posts/<str:slug>/", BlogPostDetailView.as_view()),
    # path("users/", PostUserView.as_view()),
    # path("like/", LikeView.as_view()),
    # path("all-posts/", UserAllPosts.as_view()),
    # path("posts/<str:slug>/add_comment/", CommentView.as_view()),

]
