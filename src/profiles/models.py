from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.IntegerField(verbose_name="user followers", default=0)

class Following(models.Model):
    class Meta:
        unique_together = (('follower', 'victim'),)
    follower = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="follower")
    victim = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="victim")
