import requests
from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _

from HCI_Course.settings import SETTINGS_JSON


class SignupForm(UserCreationForm):

    username = UsernameField(
        label=_("Username"),
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        label=_("Email"),
        max_length=200,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )

    def is_valid(self):
        response = self.data['g-recaptcha-response']
        key = SETTINGS_JSON['reCaptcha_key']

        r = requests.post(SETTINGS_JSON['reCaptcha_url'], {
            'secret': key,
            'response': response,
        })

        data = r.json()

        if not data['success']:
            self.add_error(None, 'reCaptcha should be validate')
            return False

        return super(SignupForm, self).is_valid()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
