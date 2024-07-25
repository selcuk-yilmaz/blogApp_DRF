from django.db import models
from django.contrib.auth.models import User


class CreateUpdateTimeField(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class BlogPost(CreateUpdateTimeField):
    STATUS = (
        ("d", "Draft"),
        ("p", "Published"),
    )

    title = models.CharField(max_length=100)
    author = models.ForeignKey(User,related_name="post_user", on_delete=models.PROTECT, default='Anonymous User')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    content = models.TextField()
    image = models.URLField(max_length=200, blank=True,
                            default="https://www.freepik.com/free-photo/teamwork-making-online-blog_11306776.htm#fromView=search&page=1&position=2&uuid=79c869b1-0b3f-451c-bd23-610137079e74")
    status = models.CharField(max_length=2, choices=STATUS)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title  


class Like(CreateUpdateTimeField):
    post = models.ForeignKey(
        BlogPost, related_name="post_like", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="user_like", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class View(CreateUpdateTimeField):
    post = models.ForeignKey(
        BlogPost, related_name="post_view", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="user_view", on_delete=models.PROTECT, null=True)


    def __str__(self):
        return f"{self.user} viewed at {self.created}"


class Comment(CreateUpdateTimeField):
    post = models.ForeignKey(
        BlogPost, related_name="post_comment", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="user_comment", on_delete=models.PROTECT, null=True)
    content = models.TextField()


    def __str__(self):
        return f"added by {self.user} at {self.created}"