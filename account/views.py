from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import UpdateView

from account.forms import SignupForm
from account.utils.email_functions import send_activation_email, account_activation_token_generator
from HCI_Course import settings
from message.utils import send_message


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(request, user)
            return render(request, 'account/message.html', {
                'title': "Sign Up Successful",
                'message': "Thank you for signing up. An activation link is sent to your email. Please Activate your "
                           "account using that link",
            })
    else:
        form = SignupForm()
    return render(request, 'account/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        user = None
    if user is not None and account_activation_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        send_message(None, user, "Welcome to WhatWeTeach")
        return render(request, 'account/activation_confirm.html')
    else:
        return render(request, 'account/message.html', {
            'title': "Something went wrong",
            'message': 'Activation link is invalid!',
        })


class UserProfileView(UpdateView):
    model = get_user_model()
    template_name = 'account/profile.html'
    success_url = reverse_lazy('account:profile')
    fields = ['username', 'first_name', 'last_name', 'email']

    def get_object(self, queryset=None):
        return self.request.user


class PasswordChangeView2(PasswordChangeView):
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change.html'


def password_change_done_view(request):
    return render(request, 'account/message.html', {
        'title': "Password Changed",
        'message': 'Your password has been successfully changed!',
    })


def forgot_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(subject_template_name='account/password_reset_email_subject.txt',
                      email_template_name='account/password_reset_email.html',
                      from_email=settings.EMAIL_PASSWORD_RESET,
                      request=request)
            return render(request, 'account/message.html', {
                'title': "Password Reset Email Sent",
                'message': 'Your password reset request has been sent to your email, '
                           'please follow the further instruction in your email',
            })
    else:
        form = PasswordResetForm()
    return render(request, 'account/forgot.html', {'form': form})


def password_reset_view(request, uidb64, token):
    def get_user():
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            return user
        return None

    def bad_token():
        return render(request, 'account/message.html', {
            'title': "Something Went Wrong :(",
            'message': 'Your token in invalid',
        })

    if request.method == 'POST':
        user = get_user()
        if not user:
            return bad_token()

        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            if not user.is_active:
                user.is_active = True
                user.save()
            return render(request, 'account/message.html', {
                'title': "Your Password Has Been Reset",
                'message': 'Your password has been reset successfully, please login with your new password',
            })
    else:
        user = get_user()
        if not user:
            return bad_token()
        form = SetPasswordForm(user)
    return render(request, 'account/password_reset.html', {'form': form})
