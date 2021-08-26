from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date, datetime

class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
    num_likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.author}: {self.content}"

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes")
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")

    def __str__(self):
        return f"{self.user} liked {self.post}"
    
class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name="followers")

    def __str__(self):
        return f"{self.user} followed {self.following}"