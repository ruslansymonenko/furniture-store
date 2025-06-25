from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from user.forms import UserLoginForm

@csrf_exempt
def login(request):
    form = UserLoginForm(data= request.POST)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:home'))

    context = {
        'title': 'Login',
        'form': form,
    }

    return render(request, 'user/login.html', context)

def registration(request):
    context = {
        'title': 'registration',
    }

    return render(request, 'user/registration.html', context)

def profile(request):
    context = {
        'title': 'profile',
    }

    return render(request, 'user/profile.html', context)

def logout(request):
    return render(request, '')

