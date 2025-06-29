from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from app.messages import SUCCESS_MESSAGES
from cart.models import Cart
from user.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, SUCCESS_MESSAGES['login_success'])

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.GET.get('next', None)

                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))

                return HttpResponseRedirect(reverse('main:home'))

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

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

        session_key = request.session.session_key

        if form.is_valid():
            form.save()
            user = form.instance

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            auth.login(request, user)
            messages.success(request, SUCCESS_MESSAGES['register_success'])

            return HttpResponseRedirect(reverse('main:home'))

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

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
            messages.success(request, SUCCESS_MESSAGES['profile_update_success'])

            return HttpResponseRedirect(reverse('user:profile'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

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
    messages.success(request, SUCCESS_MESSAGES['logout_success'])

    return redirect(reverse('main:home'))

def user_cart(request):
    return render(request, 'user/user-cart.html')