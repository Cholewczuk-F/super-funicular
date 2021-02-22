from django.db import models
from django.db.models import Q, F
from django.contrib.auth.models import User
from django.shortcuts import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.IntegerField(verbose_name="profile_followers", default=0)
    following = models.IntegerField(verbose_name="profile_following", default=0)

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'id': self.id})

    def follow(self):
        self.following += 1
    
    def get_followed(self):
        self.followers += 1


class UserFollowing(models.Model):
    profile_id = models.ForeignKey(Profile, related_name="followed_id", on_delete=models.CASCADE)
    following_profile_id = models.ForeignKey(Profile, related_name="follower_id", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ['profile_id', 'following_profile_id']
        constraints = [
            models.UniqueConstraint(fields=['profile_id','following_profile_id'],  name="unique_followers"),
            models.CheckConstraint(check=~Q(profile_id=F('following_profile_id')), name='followed_and_follower_different_constraint')
        ]

        ordering = ["-created"]


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    created = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=500, blank=True)
    likes = models.IntegerField(default=0)
    img = models.ImageField(upload_to='posts/%Y/%m/%d/%t')

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'id': self.id})
    

class PostComment(models.Model):
    # author = models.ForeignKey(Profile, verbose_name="user_id", related_name="comment_author_id", on_delete=models.DO_NOTHING)
    author = models.ForeignKey(Profile, related_name="comment_author_id", on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=500)
    likes = models.IntegerField(default=0)
    postID = models.ForeignKey(Post, on_delete=models.CASCADE)


class PostLike(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
class CommentLike(models.Model):
    comment_id = models.ForeignKey(PostComment, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)