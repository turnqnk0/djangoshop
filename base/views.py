from . import forms
from .forms import RegistrationForm, LoginForm, UserForgotPasswordForm, UserProfileForm, AddressForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.forms.models import model_to_dict
from .models import UserProfile, Address
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, urlparse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.core.files import File
from django.conf import settings
# Create your views here.


def home(request):
    context = {}
    return render(request,'base/home.html',context)


def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            if User.objects.filter(username=user_name).exists():
                form.errors['email'] = "Email already"
            elif User.objects.filter(username=user_name).exists():
                form.errors['username'] = "Username already taken"
            else:
                password = form.cleaned_data['password1']
                user = form.save()
                print(user.password)
                print(user.password)
                user.save()
                return HttpResponseRedirect(f"userprofile/{user.id}")
        return render(request, 'base/users/register.html', {'form': form})
    else:
        return render(request, 'base/users/register.html', {'form': form})


def signin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            userprofile = UserProfile.objects.get(user=user)
            address = Address.objects.get(userprofile=userprofile)
            if userprofile and address:
                auth.login(request, user)
                return render(request, 'base/home.html',
                              {'user': user, 'userprofile': userprofile, 'address': address})
    else:
        form = AuthenticationForm(request)
        return render(request, 'base/users/login.html', {"form": form})
    return render(request, 'base/users/login.html', {"form": form})


@login_required()
def user_logout(request):
    auth.logout(request)
    return redirect('/')


@login_required()
def profile_edit(request):
    if request.method == 'GET':
        user = request.user
        if user:
            userprofile = UserProfile.objects.get(user=user)
            address = Address.objects.get(userprofile=userprofile)
            address_info = model_to_dict(address, fields=('street', 'city', 'state', 'country'),
                                         exclude=('userprofile',)
                                         )
            user_info = model_to_dict(user, fields=[field.name for field in user._meta.fields],
                                      exclude=["password", "id", "is_staff", "is_superuser"]
                                      )

            print(user_info)
            return render(request, 'base/users/profile.html',
                          {"user": user, 'user_info': user_info,
                           'userprofile': userprofile.get_user_profile(), 'address': address_info})
        else:
            return render(request, 'base/users/profile.html')
    return render(request, 'base/users/profile.html', {})


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            old_password = form.clean_old_password()
            password2 = form.clean_new_password2()
            username = request.user.username
            user = auth.authenticate(username=username, password=old_password)
            if user is not None:
                user.set_password(password2)
                user.save()
                return render(request, 'base/users/solution_pages/success.html',
                              {"message": "Password changed successfully"})
            else:
                return render(request, 'base/users/passwordchange.html',
                              {'error': 'You have entered wrong old password', 'form': form})
        else:
            return render(request, 'base/users/passwordchange.html',
                          {'error': 'You have entered old password', 'form': form})
    else:
        form = PasswordChangeForm(request)
    return render(request, 'base/users/passwordchange.html', {"form": form})


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    form_user_profile = UserProfileForm()
    form_address = AddressForm()
    if request.method == 'POST':
        form_user_profile = UserProfileForm(request.POST, prefix='userprofile')
        form_address = AddressForm(request.POST, prefix='address')
        if form_user_profile.is_valid() and form_address.is_valid():
            userprofile = form_user_profile.save(commit=False)
            user.is_active = True
            userprofile.user = user
            address = form_address.save(commit=False)
            userprofile.save()
            address.userprofile = UserProfile.objects.get(user=user)
            address.save()
            return redirect('signin')
        else:
            return render(request, 'base/users/userprofile.html',
                          {"error_user_profile": form_user_profile.errors,
                           "error_address": form_address.errors})
    else:
        form_user_profile = UserProfileForm()
        form_address = AddressForm()
    return render(request, 'base/users/userprofile.html',
                  {"form_user_profile": form_user_profile, "form_address": form_address})

@login_required()
def profile_edit_page(request):
    form_userprofile = UserProfileForm()
    address_form = AddressForm()
    user = request.user
    if request.method == 'POST':
        userprofile = UserProfile.objects.get(user=user)
        address = Address.objects.get(userprofile=userprofile)
        form_userprofile = UserProfileForm(request.POST, instance=userprofile)
        address_form = AddressForm(request.POST, instance=address)
        userprofile.user = user
        address.userprofile = userprofile
        if form_userprofile.is_valid() and address_form.is_valid():
            userprofile = form_userprofile.save(commit=False)
            address = address_form.save(commit=False)
            userprofile.save()
            address.save()
            user_info = model_to_dict(user)
            return render(request, 'base/users/profile.html',
                          {'user': user_info, 'userprofile': userprofile, 'address': address})
        else:
            return render(request, 'base/users/profile_edit.html',
                          {"error_user_profile": form_userprofile.errors,
                           "error_address": address_form.errors})
    else:
        form_user_profile = UserProfileForm()
        address_form = AddressForm()
        return render(request, 'base/users/profile_edit.html',
                      {"form_user_profile": form_user_profile, "address_form": address_form})



