from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.IntegerField(verbose_name="profile_followers", default=0)
    following = models.IntegerField(verbose_name="profile_following", default=0)

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'id': self.id})

class UserFollowing(models.Model):
    user_id = models.ForeignKey(Profile, verbose_name="user_id", related_name="followed_id", on_delete=models.DO_NOTHING)
    following_user_id = models.ForeignKey(Profile, verbose_name="follower_id", related_name="follower_id", on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True, db_index=True)