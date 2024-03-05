
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django.conf import settings
from .models import UserProfile, Address
from django.forms import ModelForm


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',)


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        USERNAME_FIELD = 'username'


class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(required=True,max_length=254)

    class Meta:
        model = User
        fields = ("email",)


class AddressForm(forms.ModelForm):
    prefix = 'address'

    class Meta:
        model = Address
        fields = ('street', 'city', 'state', 'country',)


class UserProfileForm(forms.ModelForm):
    prefix = 'userprofile'

    class Meta:
        model = UserProfile
        fields = ('zipcode', 'phone', 'date_of_birth',)

