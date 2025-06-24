from django.shortcuts import render

def login(request):
    context = {
        'title': 'Login',
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

