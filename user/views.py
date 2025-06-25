from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from user.forms import UserLoginForm, UserRegistrationForm


@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)
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

            return HttpResponseRedirect(reverse('main:home'))

    else:
        form = UserRegistrationForm()

    context = {
        'title': 'registration',
        'form': form,
    }

    return render(request, 'user/registration.html', context)

def profile(request):
    context = {
        'title': 'profile',
    }

    return render(request, 'user/profile.html', context)

def logout(request):
    auth.logout(request)
    return redirect(reverse('main:home'))

