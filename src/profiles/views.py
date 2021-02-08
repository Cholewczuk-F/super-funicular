from django.shortcuts import render, redirect, HttpResponse
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .models import Profile
from .forms import UserForm, ProfileForm

def register(request):
    if request.method == "POST":
        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            p_form = p_form.save(commit=False)
            p_form.user = user
            p_form.save()
            print('Registration complete! You may log in!')
            return redirect('login')
    else:
        u_form = UserForm(request.POST or None)
        p_form = ProfileForm(request.POST or None)
        return render(request, 'registration/create_profile.html', {'u_form': u_form, 'p_form': p_form})
        
def testing(request):
    return render(request, 'base.html')

def profile_detail_view(request, id):

    try:
        int_id = int(id)
        # obj = User.objects.get(pk=int_id)
        profile = Profile.objects.get(pk=int_id)

        return HttpResponse(profile.followers)

    except User.DoesNotExist:
        raise Http404("dupa blada")

    return HttpResponse("fuck")

