from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView

from app.constants import PAGES_NAMES
from app.messages import SUCCESS_MESSAGES
from cart.models import Cart
from orders.models import Order, OrderItem
from user.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm


class UserLoginView(LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = PAGES_NAMES['login_page']
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            messages.success(self.request, SUCCESS_MESSAGES['login_success'])

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            return HttpResponseRedirect(reverse('main:home'))

        else:
            return super().form_invalid(form)

    def get_success_url(self):
        redirect_to = self.request.POST.get('next', None)

        if redirect_to and redirect_to != reverse('user:logout'):
            return redirect_to

        return reverse_lazy('main:home')

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Validation error: {error}")
        return super().form_invalid(form)


class UserRegistrationView(CreateView):
    template_name = 'user/registration.html'
    form_class = UserRegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = PAGES_NAMES['registration_page']
        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(self.request, SUCCESS_MESSAGES['register_success'])
            return HttpResponseRedirect(reverse('user:profile'))

        else:
            return super().form_invalid(form)

    def get_success_url(self):
        redirect_to = self.request.POST.get('next', None)

        if redirect_to and redirect_to != reverse('user:logout'):
            return redirect_to

        return reverse_lazy('main:home')

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Validation error: {error}")
        return super().form_invalid(form)


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'user/profile.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, SUCCESS_MESSAGES['profile_update_success'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = (
            Order.objects.filter(user=self.request.user)
                .prefetch_related(
                    Prefetch(
                        "orderitem_set",
                        queryset=OrderItem.objects.select_related("product")
                    )
                )
                .order_by('-id')
        )

        context['title'] = PAGES_NAMES['user_profile_page']
        context['orders'] = orders
        return context

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error: {error}")
        return super().form_invalid(form)


class UserCartView(TemplateView):
    template_name = 'user/user-cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = PAGES_NAMES['cart_page']
        return context


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, SUCCESS_MESSAGES['logout_success'])

    return redirect(reverse('main:home'))



