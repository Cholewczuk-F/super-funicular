from django.contrib import admin
from .models import Profile, UserFollowing, Post, PostComment, PostLike, CommentLike

admin.site.register(Profile)
admin.site.register(UserFollowing)
admin.site.register(Post)
admin.site.register(PostComment)
admin.site.register(PostLike)
admin.site.register(CommentLike)
# Register your models here. yes we know
