from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from user.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
                messages.success(request, 'You are now logged in.')

                return HttpResponseRedirect(reverse('main:home'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Login',
        'form': form,
    }

    return render(request, 'user/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            form.save()
            user = form.instance

            auth.login(request, user)
            messages.success(request, f'User {user.username} successfully registered.')

            return HttpResponseRedirect(reverse('main:home'))

    else:
        form = UserRegistrationForm()

    context = {
        'title': 'registration',
        'form': form,
    }

    return render(request, 'user/registration.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(data=request.POST, instance=request.user, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')

            return HttpResponseRedirect(reverse('user:profile'))

    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'title': 'profile',
        'form': form,
    }

    return render(request, 'user/profile.html', context)

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'Successfully logged out.')

    return redirect(reverse('main:home'))

