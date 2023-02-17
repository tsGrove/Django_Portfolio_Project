from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account has been created, you can now login.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users_forms/register.html', {'form':form})

@login_required
def profile(request):
    if request.method == 'POST':
        update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if update_form.is_valid() and profile_update_form.is_valid():
            update_form.save()
            profile_update_form.save()
            messages.success(request, f"Your account information has been updated!")
            return redirect('profile')

    else:
        update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'update_form' : update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'users_forms/profile.html', context)
