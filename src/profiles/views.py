from django.shortcuts import render, redirect, HttpResponse, reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Count

from .models import Profile, UserFollowing, Post, PostComment, PostLike, CommentLike
from .forms import UserForm, ProfileForm, PostForm, PostCommentForm

def register(request):
    if request.method == "POST":
        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)

        if u_form.is_valid() and p_form.is_valid():
            username = u_form.data["username"]
            password = u_form.data["password"]
            email = u_form.data["email"]
            first_name = u_form.data["first_name"]
            
            user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name)
            
            p_form = p_form.save(commit=False)
            p_form.user = user
            p_form.save()
            
            print('Registration complete! You may log in!')
            return redirect('login')
    else:
        u_form = UserForm(request.POST or None)
        p_form = ProfileForm(request.POST or None)
        return render(request, 'registration/create_profile.html', {'u_form': u_form, 'p_form': p_form})
        
def main_page_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        profile = Profile.objects.get(pk=request.user.pk)
        followedUsers = UserFollowing.objects.filter(following_profile_id=profile)

        for i in followedUsers:
            if Post.objects.filter(author=i.profile_id).exists():
                
                postsToView = Post.objects.filter(author=i.profile_id)[:3]
            else:
                print("followany user nie ma posta")
        
        context = {
            "profile": profile,
            "followedUsers": followedUsers,
            "postsToView": postsToView
        }
        return render(request, "profiles/user_feed.html", context)

def profile_detail_view(request, id):
    try:
        int_id = int(id)
        profile = Profile.objects.get(pk=int_id)
        is_following = False
        if request.user.is_authenticated:
            if UserFollowing.objects.filter(profile_id=profile, following_profile_id=Profile.objects.get(pk=request.user.pk)).exists():
                is_following = True

        # when clicked on follow/unfollow button
        if request.method == "POST":
            if request.user.is_authenticated:
                
                # create follow
                if not is_following:
                    UserFollowing.objects.create(profile_id=profile, following_profile_id=Profile.objects.get(pk=request.user.pk))
                    
                    # update state
                    is_following = True

                # delete follow
                else:
                    toDelete = UserFollowing.objects.get(profile_id=profile, following_profile_id=Profile.objects.get(pk=request.user.pk))
                    toDelete.delete()

                    # update state
                    is_following = True

                    
                
            # redirect to login if not authenticated
            else:
                return redirect('login')
                
        follower_count = UserFollowing.objects.filter( profile_id = profile ).count()
        following_count = UserFollowing.objects.filter( following_profile_id = profile ).count()
        context = {
            "profile": profile,
            "is_following": is_following,
            "follower_count": follower_count,
            "following_count": following_count
        }
        
        return render(request, "profiles/profile_detail.html", context)

    except User.DoesNotExist:
        raise Http404("Such profile doesn't exist.")

    return HttpResponse("The what?")


def post_detail_view(request, id):
    comment_form = PostCommentForm(request.POST or None)

    post_liked = False
    post_id = int(id)
    post = Post.objects.get(pk=post_id)
    
    if request.user.is_authenticated:
        # query user profile
        user_profile = Profile.objects.get(user=request.user.pk)

        # check if post is liked already by user
        if PostLike.objects.filter( post_id = post, user_id = user_profile ).exists():
            post_liked = True

        if request.method == "POST":
            # liking a post
            if "Unlike" in request.POST or "Like" in request.POST:
                # create like
                if not post_liked:
                    PostLike.objects.create( post_id = post, user_id = user_profile )
                    post_liked = True
                
                # delete like
                else:
                    PostLike.objects.get( post_id = post, user_id = user_profile ).delete()
                    post_liked = False

                comment_form = PostCommentForm()
                

            # post comment        
            if "Comment" in request.POST:
                description = comment_form.data['description']
                PostComment.objects.create(author=user_profile, description=description, likes=0, postID=post)


            # liking a comment
            if "commentID" in request.POST:
                com_id = request.POST["commentID"]
                tmp = PostComment.objects.get(pk=com_id)

                # create comment like
                if not CommentLike.objects.filter( comment_id = tmp, user_id = user_profile ).exists():
                    CommentLike.objects.create( comment_id = tmp, user_id = user_profile )
                # delete comment like
                else:
                    CommentLike.objects.get( comment_id = tmp, user_id = user_profile ).delete()
                
                comment_form = PostCommentForm()
                
        # if anonymous user tries to like, comment or like comment
        elif request.method == "POST":
            return redirect('login')
                  
    try:   
        # update like count
        post.likes = PostLike.objects.filter(post_id = post).count()
        post.save()

    # Query for each comments like count and relation with user
        try:
            like_counts = []
            user_likes = []
            comments = PostComment.objects.filter(postID=post_id)

            for comment in comments:
                com_is_liked = False
                if CommentLike.objects.filter( comment_id = comment, user_id = user_profile ).exists():
                    com_is_liked = True
                
                like_count = CommentLike.objects.filter(comment_id = comment).count()

                like_counts.append(like_count)
                user_likes.append(com_is_liked)

            comments_zipped = zip(comments, like_counts, user_likes)
        except PostComment.DoesNotExist:
            raise Http404("PostComments does not exist")

    except Post.DoesNotExist:
        raise Http404("Post does not exist")


    context = {
        'post': post,
        'comments': comments,
        'post_liked': post_liked,
        'comment_form': comment_form,
        'comments_zipped': comments_zipped,
    }
    
    return render(request, 'posts/post_detail.html', context)



def post_create_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)

            if form.is_valid():
                author = Profile.objects.get( user = request.user.pk )
                description = form.cleaned_data.get('description')
                img = form.cleaned_data.get('img') 
                instance = Post.objects.create( author = author, description = description, img = img )

                # redirect to freshly created post
                return redirect(reverse('post-detail', kwargs = {'id': instance.pk} ))
        else:
            form = PostForm()
        return render(request, 'posts/post_create.html', {'form': form})

    else:
        return redirect('login')