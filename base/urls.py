from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth import tokens as token
from base import views


urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('userprofile/<str:pk>', views.user_profile, name="user_profile"),
    path('signin', views.signin, name="signin"),
    path('logout', views.user_logout, name="logout"),
    path('profile', views.profile_edit, name="profile"),
    path('profile/changepass', views.change_password, name="change_pass"),
    path('profile/edit', views.profile_edit_page, name="profile_edit_page"),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='base/users/password_reset.html'),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='base/users/password_reset_done.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name=''),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]