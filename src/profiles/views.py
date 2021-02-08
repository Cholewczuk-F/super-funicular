from django.shortcuts import render
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
    return render(request, 'create_profile.html', {'u_form': u_form, 'p_form': p_form})

# Create your views here.
